from __future__ import annotations

import json
import logging
import queue
import re
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

from .data_parser import load_input_dataset
from .logger import get_logger, setup_logging
from .pipeline_orchestrator import (
    run_build_analysis_dataset_stage,
    run_infer_stage,
    run_stats_stage,
)
from .prose_analysis import warm_etymology_cache
from .utility import SUPPORTED_MODELS

logger = get_logger(__name__)


def _default_path(name: str) -> str:
    return str(Path(__file__).resolve().parents[1] / "data" / name)


def _resolve_existing_path(path_value: str) -> str:
    requested = Path(path_value).expanduser()
    if requested.exists() or requested.is_absolute():
        return str(requested)
    data_candidate = Path(__file__).resolve().parents[1] / "data" / requested
    if data_candidate.exists():
        return str(data_candidate)
    return str(requested)


def _parse_words(raw_text: str) -> list[str]:
    tokens = re.split(r"[\s,]+", raw_text.strip())
    return [token for token in tokens if token]


def _format_duration(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _format_event(event: dict[str, Any]) -> str:
    name = str(event.get("event", ""))
    parts: list[str] = []
    if name == "start":
        if "pending_model_tasks" in event:
            parts = [
                f"pending tasks: {event.get('pending_model_tasks', 0)}",
                f"screenings: {event.get('pending_screenings', 0)}",
                f"total units: {event.get('total_units', 0)}",
            ]
        elif "total_steps" in event:
            parts = [f"steps: {event.get('total_steps', 0)}"]
    elif name == "stage_start":
        parts = [f"stage={event.get('stage', '')}"]
    elif name == "stage_complete":
        parts = [f"stage={event.get('stage', '')}"]
    elif name == "screening_start":
        parts = [f"poem {event.get('poem_id', '')}"]
    elif name == "screening_complete":
        models = event.get("detected_models", [])
        parts = [
            f"poem {event.get('poem_id', '')} -> "
            + (", ".join(models) if models else "no models")
        ]
    elif name == "model_start":
        parts = [f"poem {event.get('poem_id', '')} x {event.get('model', '')}"]
    elif name == "model_complete":
        parts = [
            f"poem {event.get('poem_id', '')} x {event.get('model', '')}",
            f"{int(event.get('completed_units', 0))}/{int(event.get('total_units', 1))}",
        ]
    elif name in {"step_start", "step_complete"}:
        parts = [f"step={event.get('step', '')}"]
    elif name in {"poem_cached_skip", "poem_cached_complete"}:
        parts = [f"poem {event.get('poem_id', '')} (cached)"]
    elif name in {"complete", "error"}:
        if "message" in event:
            parts = [str(event.get("message", ""))]
        elif "error" in event:
            parts = [str(event.get("error", ""))]
    description = " | ".join(parts)
    return f"[{name}] {description}" if description else f"[{name}]"


class _QueueLogHandler(logging.Handler):
    """Forwards log records into an event queue for live display in the UI."""

    def __init__(self, event_queue: "queue.SimpleQueue[dict[str, Any]]") -> None:
        super().__init__()
        self.event_queue = event_queue

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.event_queue.put(
                {
                    "kind": "log",
                    "message": self.format(record),
                }
            )
        except Exception:
            self.handleError(record)


class _ActionWorker(threading.Thread):
    def __init__(
        self,
        *,
        action: str,
        input_path: str,
        output_path: str,
        inference_path: str,
        analysis_csv_path: str,
        output_json_path: str,
        runs_dir_path: str,
        run_id_value: str | None,
        selected_models: list[str],
        no_cache: bool,
        refresh: bool,
        max_rows: int | None,
        max_workers: int | None,
        raw_words: str,
        event_queue: "queue.SimpleQueue[dict[str, Any]]",
    ) -> None:
        super().__init__(daemon=True)
        self.action = action
        self.input_path = input_path
        self.output_path = output_path
        self.inference_path = inference_path
        self.analysis_csv_path = analysis_csv_path
        self.output_json_path = output_json_path
        self.runs_dir_path = runs_dir_path
        self.run_id_value = run_id_value
        self.selected_models = selected_models
        self.no_cache = no_cache
        self.refresh = refresh
        self.max_rows = max_rows
        self.max_workers = max_workers
        self.raw_words = raw_words
        self.event_queue = event_queue

    def _emit(self, payload: dict[str, Any]) -> None:
        self.event_queue.put(payload)

    def run(self) -> None:
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        queue_handler = _QueueLogHandler(self.event_queue)
        queue_handler.setFormatter(fmt)
        queue_handler.setLevel(logging.DEBUG)
        root_logger = logging.getLogger()
        root_logger.addHandler(queue_handler)

        def _progress_callback(event: dict[str, Any]) -> None:
            self._emit({"kind": "progress", "event": event})

        try:
            result = self._run_action(_progress_callback)
            self._emit({"kind": "result", "result": result})
        except Exception as exc:
            logger.error("Action %s failed: %s", self.action, exc, exc_info=True)
            self._emit(
                {
                    "kind": "error",
                    "error": str(exc),
                    "trace": traceback.format_exc(),
                }
            )
        finally:
            root_logger.removeHandler(queue_handler)
            self._emit({"kind": "done"})

    def _run_action(self, progress_callback: Any) -> dict[str, Any]:
        if self.action == "infer":
            return run_infer_stage(
                input_csv=self.input_path,
                output_csv=self.output_path,
                models=self.selected_models,
                check_cache=not self.no_cache,
                max_rows=self.max_rows,
                max_workers=self.max_workers,
                runs_dir=self.runs_dir_path,
                run_id=self.run_id_value,
                default_output_csv=_default_path("inference_results.csv"),
                progress_callback=progress_callback,
            )
        if self.action == "stats":
            return run_stats_stage(
                input_csv=self.input_path,
                inference_csv=self.inference_path,
                analysis_csv=self.analysis_csv_path,
                output_json=self.output_json_path,
                report_md=None,
                runs_dir=self.runs_dir_path,
                run_id=self.run_id_value,
                default_inference_csv=_default_path("inference_results.csv"),
                default_analysis_csv=_default_path("analysis_dataset.csv"),
                default_output_json=_default_path("statistical_results.json"),
                progress_callback=progress_callback,
            )
        if self.action == "build-analysis-dataset":
            return run_build_analysis_dataset_stage(
                input_csv=self.input_path,
                inference_csv=self.inference_path,
                analysis_csv=self.analysis_csv_path,
                runs_dir=self.runs_dir_path,
                run_id=self.run_id_value,
                default_inference_csv=_default_path("inference_results.csv"),
                default_analysis_csv=_default_path("analysis_dataset.csv"),
            )
        if self.action == "warm-etymology-cache":
            words = (
                _parse_words(self.raw_words)
                if self.raw_words.strip()
                else load_input_dataset(self.input_path)["poem_text"].fillna("").tolist()
            )
            raw_result = warm_etymology_cache(words, refresh=self.refresh)
            return {"action": self.action, **raw_result}
        if self.action == "full-stack-run":
            self._emit({"kind": "progress", "event": {"event": "stage_start", "stage": "infer"}})
            infer_result = run_infer_stage(
                input_csv=self.input_path,
                output_csv=self.output_path,
                models=self.selected_models,
                check_cache=not self.no_cache,
                max_rows=self.max_rows,
                max_workers=self.max_workers,
                runs_dir=self.runs_dir_path,
                run_id=self.run_id_value,
                default_output_csv=_default_path("inference_results.csv"),
                progress_callback=progress_callback,
            )
            self._emit({"kind": "progress", "event": {"event": "stage_complete", "stage": "infer"}})

            resolved_run_id = str(infer_result.get("run_id"))
            self._emit({"kind": "progress", "event": {"event": "stage_start", "stage": "stats", "run_id": resolved_run_id}})
            stats_result = run_stats_stage(
                input_csv=self.input_path,
                inference_csv=self.inference_path,
                analysis_csv=self.analysis_csv_path,
                output_json=self.output_json_path,
                report_md=None,
                runs_dir=self.runs_dir_path,
                run_id=resolved_run_id,
                default_inference_csv=_default_path("inference_results.csv"),
                default_analysis_csv=_default_path("analysis_dataset.csv"),
                default_output_json=_default_path("statistical_results.json"),
                progress_callback=progress_callback,
            )
            self._emit({"kind": "progress", "event": {"event": "stage_complete", "stage": "stats", "run_id": resolved_run_id}})
            return {
                "action": "full-stack-run",
                "run_id": resolved_run_id,
                "infer": infer_result,
                "stats": stats_result,
            }
        raise ValueError(f"Unsupported action: {self.action}")


class _CommandCenterWindow:  # pragma: no cover - exercised manually
    def __init__(self, defaults: dict[str, Any], qt: dict[str, Any]) -> None:
        self.QtCore = qt["QtCore"]
        self.QtWidgets = qt["QtWidgets"]

        self.event_queue: "queue.SimpleQueue[dict[str, Any]]" = queue.SimpleQueue()
        self.worker: _ActionWorker | None = None
        self.started_at = 0.0
        self.progress_state: dict[str, Any] = {"phase": "idle", "total": 0, "completed": 0}
        self.last_result: dict[str, Any] | None = None

        self.window = self.QtWidgets.QMainWindow()
        self.window.setWindowTitle("Literary Analysis - Command Center")
        self.window.resize(1320, 860)

        central = self.QtWidgets.QWidget()
        self.window.setCentralWidget(central)
        outer_layout = self.QtWidgets.QVBoxLayout(central)

        form_layout = self.QtWidgets.QGridLayout()
        outer_layout.addLayout(form_layout)

        self.action_combo = self.QtWidgets.QComboBox()
        self.action_combo.addItems([
            "infer",
            "stats",
            "build-analysis-dataset",
            "warm-etymology-cache",
            "full-stack-run",
        ])

        self.no_cache_checkbox = self.QtWidgets.QCheckBox("No cache (infer)")
        self.refresh_checkbox = self.QtWidgets.QCheckBox("Refresh etymology cache")

        self.input_edit = self.QtWidgets.QLineEdit(str(defaults["input"]))
        self.output_edit = self.QtWidgets.QLineEdit(str(defaults["output"]))
        self.inference_edit = self.QtWidgets.QLineEdit(str(defaults["inference"]))
        self.analysis_edit = self.QtWidgets.QLineEdit(str(defaults["analysis_csv"]))
        self.output_json_edit = self.QtWidgets.QLineEdit(str(defaults["output_json"]))
        self.runs_dir_edit = self.QtWidgets.QLineEdit(str(defaults["runs_dir"]))
        self.run_id_edit = self.QtWidgets.QLineEdit(str(defaults["run_id"]))

        self.max_rows_spin = self.QtWidgets.QSpinBox()
        self.max_rows_spin.setRange(0, 10_000_000)
        self.max_rows_spin.setValue(int(defaults.get("max_rows", 0)))

        self.max_workers_spin = self.QtWidgets.QSpinBox()
        self.max_workers_spin.setRange(0, 1024)
        self.max_workers_spin.setValue(int(defaults.get("max_workers", 0)))

        self.words_edit = self.QtWidgets.QPlainTextEdit()
        self.words_edit.setPlaceholderText("Words for warm-etymology-cache (comma or space separated)")
        self.words_edit.setFixedHeight(80)

        self.model_checks: dict[str, Any] = {}
        model_box = self.QtWidgets.QGroupBox("Models (infer)")
        model_layout = self.QtWidgets.QGridLayout(model_box)
        for index, model in enumerate(SUPPORTED_MODELS):
            check = self.QtWidgets.QCheckBox(model)
            if model in defaults["models"]:
                check.setChecked(True)
            model_layout.addWidget(check, index // 3, index % 3)
            self.model_checks[model] = check

        form_layout.addWidget(self.QtWidgets.QLabel("Action"), 0, 0)
        form_layout.addWidget(self.action_combo, 0, 1)
        form_layout.addWidget(self.no_cache_checkbox, 0, 2)
        form_layout.addWidget(self.refresh_checkbox, 0, 3)

        form_layout.addWidget(self.QtWidgets.QLabel("Input CSV"), 1, 0)
        form_layout.addWidget(self.input_edit, 1, 1, 1, 3)

        form_layout.addWidget(self.QtWidgets.QLabel("Output CSV (infer)"), 2, 0)
        form_layout.addWidget(self.output_edit, 2, 1, 1, 3)

        form_layout.addWidget(self.QtWidgets.QLabel("Inference CSV (stats/build)"), 3, 0)
        form_layout.addWidget(self.inference_edit, 3, 1, 1, 3)

        form_layout.addWidget(self.QtWidgets.QLabel("Analysis CSV"), 4, 0)
        form_layout.addWidget(self.analysis_edit, 4, 1, 1, 3)

        form_layout.addWidget(self.QtWidgets.QLabel("Output JSON (stats)"), 5, 0)
        form_layout.addWidget(self.output_json_edit, 5, 1, 1, 3)

        form_layout.addWidget(self.QtWidgets.QLabel("Runs Directory"), 6, 0)
        form_layout.addWidget(self.runs_dir_edit, 6, 1)
        form_layout.addWidget(self.QtWidgets.QLabel("Run ID (optional)"), 6, 2)
        form_layout.addWidget(self.run_id_edit, 6, 3)

        form_layout.addWidget(self.QtWidgets.QLabel("Max Rows (0=all)"), 7, 0)
        form_layout.addWidget(self.max_rows_spin, 7, 1)
        form_layout.addWidget(self.QtWidgets.QLabel("Max Workers (0=auto)"), 7, 2)
        form_layout.addWidget(self.max_workers_spin, 7, 3)

        outer_layout.addWidget(model_box)
        outer_layout.addWidget(self.words_edit)

        controls_layout = self.QtWidgets.QHBoxLayout()
        outer_layout.addLayout(controls_layout)

        self.run_button = self.QtWidgets.QPushButton("Run Action")
        self.run_button.clicked.connect(self._start_run)
        controls_layout.addWidget(self.run_button)

        self.status_label = self.QtWidgets.QLabel("Status: idle")
        self.phase_label = self.QtWidgets.QLabel("Phase: idle")
        self.eta_label = self.QtWidgets.QLabel("ETA: --")
        self.elapsed_label = self.QtWidgets.QLabel("Elapsed: 00:00")
        self.rate_label = self.QtWidgets.QLabel("Rate: --")
        controls_layout.addWidget(self.status_label)
        controls_layout.addWidget(self.phase_label)
        controls_layout.addWidget(self.eta_label)
        controls_layout.addWidget(self.elapsed_label)
        controls_layout.addWidget(self.rate_label)

        self.progress_bar = self.QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        outer_layout.addWidget(self.progress_bar)

        split = self.QtWidgets.QSplitter()
        split.setOrientation(self.QtCore.Qt.Orientation.Horizontal)
        outer_layout.addWidget(split, stretch=1)

        self.log_output = self.QtWidgets.QPlainTextEdit()
        self.log_output.setReadOnly(True)
        split.addWidget(self.log_output)

        right_tabs = self.QtWidgets.QTabWidget()
        split.addWidget(right_tabs)
        split.setStretchFactor(0, 2)
        split.setStretchFactor(1, 1)

        self.summary_output = self.QtWidgets.QPlainTextEdit()
        self.summary_output.setReadOnly(True)
        right_tabs.addTab(self.summary_output, "Summary")

        artifacts_widget = self.QtWidgets.QWidget()
        artifacts_layout = self.QtWidgets.QVBoxLayout(artifacts_widget)
        self.artifact_list = self.QtWidgets.QListWidget()
        self.artifact_list.itemSelectionChanged.connect(self._show_selected_artifact)
        artifacts_layout.addWidget(self.artifact_list)
        self.artifact_preview = self.QtWidgets.QPlainTextEdit()
        self.artifact_preview.setReadOnly(True)
        artifacts_layout.addWidget(self.artifact_preview)
        right_tabs.addTab(artifacts_widget, "Artifacts")

        self.timer = self.QtCore.QTimer()
        self.timer.setInterval(150)
        self.timer.timeout.connect(self._drain_events)
        self.timer.start()

    def show(self) -> None:
        self.window.show()

    def _append_line(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.appendPlainText(f"[{timestamp}] {message}")
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def _selected_models(self) -> list[str]:
        return [model for model, check in self.model_checks.items() if check.isChecked()]

    def _start_run(self) -> None:
        if self.worker is not None and self.worker.is_alive():
            self._append_line("A run is already in progress.")
            return

        action = self.action_combo.currentText().strip()
        selected_models = self._selected_models()
        if action in {"infer", "full-stack-run"} and not selected_models:
            self._append_line("Validation error: select at least one model for infer/full-stack-run.")
            self.status_label.setText("Status: validation failed")
            return

        max_rows = int(self.max_rows_spin.value()) or None
        max_workers = int(self.max_workers_spin.value()) or None

        run_id_value = self.run_id_edit.text().strip() or None
        input_resolved = _resolve_existing_path(self.input_edit.text().strip())
        inference_resolved = _resolve_existing_path(self.inference_edit.text().strip())

        self.progress_state = {"phase": f"{action} / starting", "total": 0, "completed": 0}
        self.started_at = time.perf_counter()
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Status: running {action}")
        self.phase_label.setText(f"Phase: {self.progress_state['phase']}")
        self.summary_output.setPlainText("")
        self.artifact_list.clear()
        self.artifact_preview.setPlainText("")

        self.worker = _ActionWorker(
            action=action,
            input_path=input_resolved,
            output_path=self.output_edit.text().strip(),
            inference_path=inference_resolved,
            analysis_csv_path=self.analysis_edit.text().strip(),
            output_json_path=self.output_json_edit.text().strip(),
            runs_dir_path=self.runs_dir_edit.text().strip(),
            run_id_value=run_id_value,
            selected_models=selected_models,
            no_cache=bool(self.no_cache_checkbox.isChecked()),
            refresh=bool(self.refresh_checkbox.isChecked()),
            max_rows=max_rows,
            max_workers=max_workers,
            raw_words=self.words_edit.toPlainText(),
            event_queue=self.event_queue,
        )
        self.worker.start()
        self._append_line(f"[{action}] started")

    def _drain_events(self) -> None:
        saw_done = False
        while True:
            try:
                item = self.event_queue.get_nowait()
            except queue.Empty:
                break
            kind = str(item.get("kind", ""))
            if kind == "log":
                self._append_line(str(item.get("message", "")))
            elif kind == "progress":
                event = item.get("event", {})
                if isinstance(event, dict):
                    self._apply_progress_event(event)
                    self._append_line(_format_event(event))
            elif kind == "result":
                result = item.get("result", {})
                self.last_result = result if isinstance(result, dict) else None
                self._append_line("result:")
                self._append_line(json.dumps(result, indent=2))
                self._render_result_panels(result)
                self.status_label.setText("Status: completed")
            elif kind == "error":
                self._append_line(f"error: {item.get('error', 'unknown error')}")
                trace = str(item.get("trace", ""))
                if trace:
                    self._append_line(trace)
                self.status_label.setText("Status: failed")
            elif kind == "done":
                saw_done = True

        self._refresh_timing()

        if saw_done:
            if self.progress_state.get("total", 0) > 0:
                self.progress_state["completed"] = self.progress_state["total"]
                self.progress_bar.setValue(100)
            self.phase_label.setText(f"Phase: {self.progress_state.get('phase', 'done')}")

    def _apply_progress_event(self, event: dict[str, Any]) -> None:
        event_name = str(event.get("event", ""))
        self.progress_state["phase"] = _format_event(event)

        if "total_units" in event:
            self.progress_state["total"] = max(0, int(event.get("total_units", 0)))
        if "completed_units" in event:
            self.progress_state["completed"] = max(0, int(event.get("completed_units", 0)))

        if "total_steps" in event:
            self.progress_state["total"] = max(0, int(event.get("total_steps", 0)))
        if "completed_steps" in event:
            self.progress_state["completed"] = max(0, int(event.get("completed_steps", 0)))

        if event_name == "complete" and int(self.progress_state.get("total", 0)) > 0:
            self.progress_state["completed"] = int(self.progress_state["total"])
        if event_name == "error":
            self.status_label.setText("Status: failed")

        total = int(self.progress_state.get("total", 0))
        completed = int(self.progress_state.get("completed", 0))
        percent = int(min(100, max(0, (completed / total) * 100))) if total > 0 else 0
        self.progress_bar.setValue(percent)
        self.phase_label.setText(f"Phase: {self.progress_state['phase']}")

    def _refresh_timing(self) -> None:
        if self.started_at <= 0:
            return
        elapsed = max(0.0, time.perf_counter() - self.started_at)
        total = int(self.progress_state.get("total", 0))
        completed = int(self.progress_state.get("completed", 0))
        eta_text = "--"
        rate_text = "--"
        if elapsed > 0 and completed > 0:
            rate = completed / elapsed
            rate_text = f"{rate:.2f} units/s"
            if total > completed and rate > 0:
                eta_text = _format_duration((total - completed) / rate)
            elif total > 0:
                eta_text = "00:00"
        self.eta_label.setText(f"ETA: {eta_text}")
        self.elapsed_label.setText(f"Elapsed: {_format_duration(elapsed)}")
        self.rate_label.setText(f"Rate: {rate_text}")

    def _result_artifact_paths(self, payload: Any) -> list[Path]:
        paths: list[Path] = []

        def _collect(node: Any) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        _collect(value)
                    elif isinstance(value, str):
                        if key.endswith(("_csv", "_json", "_md")) or key in {"output", "inference", "analysis_csv", "output_json", "report_md"}:
                            candidate = Path(value)
                            if candidate.exists():
                                paths.append(candidate)
            elif isinstance(node, list):
                for item in node:
                    _collect(item)

        _collect(payload)
        deduped: list[Path] = []
        seen: set[str] = set()
        for path in paths:
            resolved = str(path.resolve())
            if resolved in seen:
                continue
            seen.add(resolved)
            deduped.append(path)
        return deduped

    def _build_stats_summary_text(self, results: dict[str, Any]) -> str:
        lines: list[str] = []
        metrics = results.get("score_model_comparisons_by_metric", {}).get("metrics", {})
        lines.append("Significant model differences by metric (alpha=0.05):")
        any_score = False
        for metric in ("aggregate_score", "technical_craft_score", "structure_score", "diction_score", "originality_score", "impact_score"):
            payload = metrics.get(metric, {})
            pairwise = [
                row for row in payload.get("pairwise", [])
                if row.get("status") == "ok" and row.get("significant")
            ]
            if not pairwise:
                continue
            any_score = True
            lines.append(f"- {metric}:")
            for row in pairwise:
                lines.append(
                    f"  {row.get('left_model')} vs {row.get('right_model')}: "
                    f"{row.get('direction')} (mean diff {float(row.get('mean_difference', 0.0)):+.3f}, "
                    f"adj p={row.get('adjusted_pvalue'):.4f})"
                )
        if not any_score:
            lines.append("- none")

        lines.append("")
        lines.append("Significant interaction directions:")
        any_interactions = False
        for family_key, label_key in (
            ("device_score_interactions_by_metric", "device"),
            ("diction_score_interactions_by_metric", "feature"),
            ("author_score_interactions_by_metric", "feature"),
        ):
            metrics_payload = results.get(family_key, {}).get("metrics", {})
            for metric, payload in metrics_payload.items():
                for row in payload.get("tests", []):
                    if row.get("status") == "ok" and row.get("significant"):
                        any_interactions = True
                        label = row.get(label_key, "unknown")
                        lines.append(
                            f"- {family_key}/{metric}/{label}: {row.get('direction_summary', 'direction unavailable')}"
                        )
        if not any_interactions:
            lines.append("- none")
        return "\n".join(lines)

    def _find_stats_json_from_result(self, result: dict[str, Any]) -> Path | None:
        if result.get("action") == "stats":
            candidate = Path(str(result.get("output_json", "")))
            if candidate.exists():
                return candidate
        if result.get("action") == "full-stack-run":
            stats = result.get("stats", {})
            candidate = Path(str(stats.get("output_json", "")))
            if candidate.exists():
                return candidate
        return None

    def _render_result_panels(self, result: dict[str, Any]) -> None:
        self.artifact_list.clear()
        for path in self._result_artifact_paths(result):
            self.artifact_list.addItem(str(path))

        summary_lines = ["Run complete.", "", "Top-level result:", json.dumps(result, indent=2)]
        stats_json = self._find_stats_json_from_result(result)
        if stats_json is not None:
            try:
                stats_payload = json.loads(stats_json.read_text(encoding="utf-8"))
                summary_lines = [self._build_stats_summary_text(stats_payload)]
            except Exception as exc:
                summary_lines.append(f"\nCould not parse stats payload: {exc}")
        self.summary_output.setPlainText("\n".join(summary_lines))

    def _show_selected_artifact(self) -> None:
        items = self.artifact_list.selectedItems()
        if not items:
            self.artifact_preview.setPlainText("")
            return
        path = Path(items[0].text())
        if not path.exists():
            self.artifact_preview.setPlainText(f"Missing file: {path}")
            return
        if path.suffix.lower() in {".json", ".md", ".txt", ".csv"}:
            try:
                content = path.read_text(encoding="utf-8")
                if len(content) > 50_000:
                    content = content[:50_000] + "\n\n[truncated]"
                self.artifact_preview.setPlainText(content)
                return
            except Exception as exc:
                self.artifact_preview.setPlainText(f"Unable to open text file: {exc}")
                return
        self.artifact_preview.setPlainText(f"Preview not supported for file type: {path.suffix}")


def launch_command_center(defaults: dict | None = None) -> None:
    try:
        from PySide6 import QtCore, QtWidgets
    except ImportError as exc:
        raise RuntimeError("PySide6 is required: pip install PySide6") from exc

    setup_logging()
    logger.info("Launching command center")

    values: dict[str, Any] = {
        "input": _default_path("input.csv"),
        "inference": _default_path("inference_results.csv"),
        "output": _default_path("inference_results.csv"),
        "analysis_csv": _default_path("analysis_dataset.csv"),
        "output_json": _default_path("statistical_results.json"),
        "runs_dir": _default_path("runs"),
        "run_id": "",
        "models": list(SUPPORTED_MODELS),
        "max_rows": 0,
        "max_workers": 0,
    }
    if defaults:
        values.update(defaults)

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    window = _CommandCenterWindow(values, {"QtCore": QtCore, "QtWidgets": QtWidgets})
    window.show()
    app.exec()

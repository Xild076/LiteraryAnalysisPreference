from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Callable

if __package__ in {None, ""}:
    import sys

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    from src.command_center import launch_command_center
    from src.data_parser import load_input_dataset
    from src.pipeline_orchestrator import (
        run_build_analysis_dataset_stage,
        run_infer_stage,
        run_stats_stage,
    )
    from src.prose_analysis import warm_etymology_cache
    from src.utility import SUPPORTED_MODELS
else:
    from .command_center import launch_command_center
    from .data_parser import load_input_dataset
    from .pipeline_orchestrator import (
        run_build_analysis_dataset_stage,
        run_infer_stage,
        run_stats_stage,
    )
    from .prose_analysis import warm_etymology_cache
    from .utility import SUPPORTED_MODELS


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


class _TerminalProgressBar:
    def __init__(self) -> None:
        self.enabled = sys.stdout.isatty()
        self._max_rendered_width = 0
        self._active = False

    def update(self, label: str, completed: int, total: int) -> None:
        if not self.enabled:
            return
        safe_total = max(int(total), 1)
        safe_completed = min(max(int(completed), 0), safe_total)
        fraction = safe_completed / safe_total
        bar_width = 30
        filled = int(round(fraction * bar_width))
        bar = f"{'#' * filled}{'-' * (bar_width - filled)}"
        line = f"{label:<18} [{bar}] {safe_completed}/{safe_total} ({fraction * 100:5.1f}%)"
        self._max_rendered_width = max(self._max_rendered_width, len(line))
        print(f"\r{line.ljust(self._max_rendered_width)}", end="", flush=True)
        self._active = True

    def finish(self, message: str) -> None:
        if not self.enabled:
            return
        padded = message.ljust(max(self._max_rendered_width, len(message)))
        if self._active:
            print(f"\r{padded}")
        else:
            print(padded)
        self._active = False


def _infer_progress_callback(progress_bar: _TerminalProgressBar) -> Callable[[dict[str, Any]], None]:
    def _callback(event: dict[str, Any]) -> None:
        total_units = event.get("total_units")
        completed_units = event.get("completed_units")
        if total_units is not None and completed_units is not None:
            event_name = str(event.get("event", ""))
            if event_name.startswith("screening"):
                label = "Infer screening"
            elif event_name.startswith("persist"):
                label = "Infer persist"
            elif event_name.startswith("model"):
                label = "Infer models"
            else:
                label = "Inference"
            progress_bar.update(label, int(completed_units), int(total_units))

    return _callback


def _stats_progress_callback(progress_bar: _TerminalProgressBar) -> Callable[[dict[str, Any]], None]:
    def _callback(event: dict[str, Any]) -> None:
        event_name = str(event.get("event", ""))
        if event_name in {"start", "step_start", "step_complete", "complete", "error"}:
            total_steps = event.get("total_steps")
            completed_steps = event.get("completed_steps")
            if total_steps is not None and completed_steps is not None:
                progress_bar.update("Stats steps", int(completed_steps), int(total_steps))
            return

        if event_name in {"feature_start", "feature_progress"}:
            total_rows = event.get("total_feature_rows")
            completed_rows = event.get("completed_feature_rows")
            if total_rows is not None and completed_rows is not None:
                progress_bar.update("Feature calc", int(completed_rows), int(total_rows))

    return _callback


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Literary analysis pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    infer_parser = subparsers.add_parser("infer", help="Run model inference across the poem dataset")
    infer_parser.add_argument("--input", default=_default_path("input.csv"))
    infer_parser.add_argument("--output", default=_default_path("inference_results.csv"))
    infer_parser.add_argument("--models", nargs="+", default=list(SUPPORTED_MODELS))
    infer_parser.add_argument("--no-cache", action="store_true")
    infer_parser.add_argument("--max-rows", type=int, default=0, help="Limit dataset to first N rows (0 = all)")
    infer_parser.add_argument("--max-workers", type=int, default=0, help="Parallel model workers per poem (0 = auto)")
    infer_parser.add_argument("--sample-size", type=int, default=0, help="Randomly sample N poems before inference (0 = all)")
    infer_parser.add_argument("--sample-seed", type=int, default=0, help="Optional random seed for inference sampling")
    infer_parser.add_argument("--runs-dir", default=_default_path("runs"))
    infer_parser.add_argument("--run-id")

    stats_parser = subparsers.add_parser("stats", help="Build the analysis dataset and run statistical tests")
    stats_parser.add_argument("--input", default=_default_path("input.csv"))
    stats_parser.add_argument("--inference", default=_default_path("inference_results.csv"))
    stats_parser.add_argument("--analysis-csv", default=_default_path("analysis_dataset.csv"))
    stats_parser.add_argument("--output-json", default=_default_path("statistical_results.json"))
    stats_parser.add_argument("--report-md")
    stats_parser.add_argument("--sample-poems", type=int, default=0, help="Randomly sample N balanced poems for stats (0 = all)")
    stats_parser.add_argument("--sample-seed", type=int, default=0, help="Optional random seed for stats sampling")
    stats_parser.add_argument("--runs-dir", default=_default_path("runs"))
    stats_parser.add_argument("--run-id")

    warm_parser = subparsers.add_parser("warm-etymology-cache", help="Warm the permanent etymology cache")
    warm_parser.add_argument("--input", default=_default_path("input.csv"))
    warm_parser.add_argument("--refresh", action="store_true")
    warm_parser.add_argument("words", nargs="*")

    dataset_parser = subparsers.add_parser("build-analysis-dataset", help="Build the joined analysis dataset without running tests")
    dataset_parser.add_argument("--input", default=_default_path("input.csv"))
    dataset_parser.add_argument("--inference", default=_default_path("inference_results.csv"))
    dataset_parser.add_argument("--analysis-csv", default=_default_path("analysis_dataset.csv"))
    dataset_parser.add_argument("--sample-poems", type=int, default=0, help="Randomly sample N balanced poems for analysis dataset (0 = all)")
    dataset_parser.add_argument("--sample-seed", type=int, default=0, help="Optional random seed for analysis sampling")
    dataset_parser.add_argument("--runs-dir", default=_default_path("runs"))
    dataset_parser.add_argument("--run-id")

    ui_parser = subparsers.add_parser("command-center", help="Launch the desktop command center UI")
    ui_parser.add_argument("--input", default=_default_path("input.csv"))
    ui_parser.add_argument("--inference", default=_default_path("inference_results.csv"))
    ui_parser.add_argument("--output", default=_default_path("inference_results.csv"))
    ui_parser.add_argument("--analysis-csv", default=_default_path("analysis_dataset.csv"))
    ui_parser.add_argument("--output-json", default=_default_path("statistical_results.json"))
    ui_parser.add_argument("--models", nargs="+", default=list(SUPPORTED_MODELS))
    ui_parser.add_argument("--max-workers", type=int, default=0)
    ui_parser.add_argument("--runs-dir", default=_default_path("runs"))
    ui_parser.add_argument("--run-id")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "infer":
        input_path = _resolve_existing_path(args.input)
        max_rows = int(args.max_rows) if args.max_rows and args.max_rows > 0 else None
        max_workers = int(args.max_workers) if args.max_workers and args.max_workers > 0 else None
        sample_size = int(args.sample_size) if args.sample_size and args.sample_size > 0 else None
        sample_seed = int(args.sample_seed) if args.sample_seed and args.sample_seed > 0 else None
        progress_bar = _TerminalProgressBar()
        payload = run_infer_stage(
            input_csv=input_path,
            output_csv=args.output,
            models=list(args.models),
            check_cache=not args.no_cache,
            max_rows=max_rows,
            max_workers=max_workers,
            sample_size=sample_size,
            sample_seed=sample_seed,
            runs_dir=args.runs_dir,
            run_id=args.run_id,
            default_output_csv=_default_path("inference_results.csv"),
            progress_callback=_infer_progress_callback(progress_bar),
        )
        progress_bar.finish("Inference complete")
        print(json.dumps(payload, indent=2))
        return

    if args.command == "stats":
        input_path = _resolve_existing_path(args.input)
        inference_path = _resolve_existing_path(args.inference)
        sample_poems = int(args.sample_poems) if args.sample_poems and args.sample_poems > 0 else None
        sample_seed = int(args.sample_seed) if args.sample_seed and args.sample_seed > 0 else None
        progress_bar = _TerminalProgressBar()
        payload = run_stats_stage(
            input_csv=input_path,
            inference_csv=inference_path,
            analysis_csv=args.analysis_csv,
            output_json=args.output_json,
            report_md=args.report_md,
            runs_dir=args.runs_dir,
            run_id=args.run_id,
            default_inference_csv=_default_path("inference_results.csv"),
            default_analysis_csv=_default_path("analysis_dataset.csv"),
            default_output_json=_default_path("statistical_results.json"),
            sample_poems=sample_poems,
            sample_seed=sample_seed,
            progress_callback=_stats_progress_callback(progress_bar),
        )
        progress_bar.finish("Stats complete")
        print(json.dumps(payload, indent=2))
        return

    if args.command == "warm-etymology-cache":
        if args.words:
            payload = args.words
        else:
            input_path = _resolve_existing_path(args.input)
            payload = load_input_dataset(input_path)["poem_text"].fillna("").tolist()
        result = warm_etymology_cache(payload, refresh=args.refresh)
        print(json.dumps(result, indent=2))
        return

    if args.command == "build-analysis-dataset":
        input_path = _resolve_existing_path(args.input)
        inference_path = _resolve_existing_path(args.inference)
        sample_poems = int(args.sample_poems) if args.sample_poems and args.sample_poems > 0 else None
        sample_seed = int(args.sample_seed) if args.sample_seed and args.sample_seed > 0 else None
        progress_bar = _TerminalProgressBar()
        payload = run_build_analysis_dataset_stage(
            input_csv=input_path,
            inference_csv=inference_path,
            analysis_csv=args.analysis_csv,
            runs_dir=args.runs_dir,
            run_id=args.run_id,
            default_inference_csv=_default_path("inference_results.csv"),
            default_analysis_csv=_default_path("analysis_dataset.csv"),
            sample_poems=sample_poems,
            sample_seed=sample_seed,
            progress_callback=_stats_progress_callback(progress_bar),
        )
        progress_bar.finish("Analysis dataset complete")
        print(json.dumps(payload, indent=2))
        return

    if args.command == "command-center":
        launch_command_center(
            {
                "input": _resolve_existing_path(args.input),
                "inference": _resolve_existing_path(args.inference),
                "output": args.output,
                "analysis_csv": args.analysis_csv,
                "output_json": args.output_json,
                "models": list(args.models),
                "max_workers": int(args.max_workers) if args.max_workers and args.max_workers > 0 else 0,
                "runs_dir": args.runs_dir,
                "run_id": args.run_id or "",
            }
        )
        return

    parser.error(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()

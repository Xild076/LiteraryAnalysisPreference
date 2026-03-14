from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pandas as pd

from .artifacts import RunArtifactsManager
from .inference import run_inference_on_dataset
from .statistical_analysis import build_analysis_dataset, run_all_analyses

INFERENCE_ARTIFACT = "inference_results.csv"
ANALYSIS_ARTIFACT = "analysis_dataset.csv"
STATS_JSON_ARTIFACT = "statistical_results.json"
STATS_MD_ARTIFACT = "statistical_report.md"


def _same_path(left: str | Path, right: str | Path) -> bool:
    left_path = Path(left)
    right_path = Path(right)
    try:
        return left_path.resolve() == right_path.resolve()
    except FileNotFoundError:
        return left_path.absolute() == right_path.absolute()


def _prefer_run_input_path(
    provided_path: str,
    default_path: str,
    run_artifact_path: Path,
) -> str:
    if _same_path(provided_path, default_path) and run_artifact_path.exists():
        return str(run_artifact_path)
    return provided_path


def _effective_output_path(
    requested_path: str,
    default_path: str,
    run_artifact_path: Path,
    run_id: str | None,
) -> str:
    if run_id is not None and _same_path(requested_path, default_path):
        return str(run_artifact_path)
    return requested_path


def run_infer_stage(
    *,
    input_csv: str,
    output_csv: str,
    models: list[str],
    check_cache: bool,
    runs_dir: str,
    run_id: str | None,
    default_output_csv: str,
    max_rows: int | None = None,
    max_workers: int | None = None,
    sample_size: int | None = None,
    sample_seed: int | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    manager = RunArtifactsManager(runs_dir)
    context = manager.prepare_run(run_id)
    run_output_path = manager.artifact_path(context, INFERENCE_ARTIFACT)
    effective_output_path = _effective_output_path(output_csv, default_output_csv, run_output_path, run_id)

    try:
        inference_kwargs: dict[str, Any] = {"check_cache": check_cache}
        if max_rows is not None:
            inference_kwargs["max_rows"] = max_rows
        if max_workers is not None:
            inference_kwargs["max_workers"] = max_workers
        if sample_size is not None:
            inference_kwargs["sample_size"] = sample_size
        if sample_seed is not None:
            inference_kwargs["sample_seed"] = sample_seed
        if progress_callback is not None:
            inference_kwargs["progress_callback"] = progress_callback
        df = run_inference_on_dataset(input_csv, effective_output_path, models, **inference_kwargs)
        manager.mirror_artifact(effective_output_path, run_output_path)
        manager.mirror_artifact(run_output_path, output_csv)
        manifest_path = manager.record_stage(
            context,
            "infer",
            "ok",
            {
                "inputs": {"input_csv": str(Path(input_csv))},
                "outputs": {
                    "requested_output_csv": str(Path(output_csv)),
                    "run_output_csv": str(run_output_path),
                },
                "models": list(models),
                "rows": int(len(df)),
                "cache_enabled": bool(check_cache),
                "sample_size": sample_size,
                "sample_seed": sample_seed,
            },
        )
        return {
            "action": "infer",
            "rows": int(len(df)),
            "input": str(Path(input_csv)),
            "output": str(Path(output_csv)),
            "models": list(models),
            "run_id": context.run_id,
            "run_dir": str(context.run_dir),
            "artifacts": {
                "manifest_json": str(manifest_path),
                "inference_csv": str(run_output_path),
            },
        }
    except Exception as exc:
        manifest_path = manager.record_stage(
            context,
            "infer",
            "error",
            {
                "inputs": {"input_csv": str(Path(input_csv))},
                "outputs": {
                    "requested_output_csv": str(Path(output_csv)),
                    "run_output_csv": str(run_output_path),
                },
                "models": list(models),
                "cache_enabled": bool(check_cache),
                "sample_size": sample_size,
                "sample_seed": sample_seed,
                "error": str(exc),
            },
        )
        raise RuntimeError(
            f"Infer stage failed. Run: {context.run_id}. Manifest: {manifest_path}. Error: {exc}"
        ) from exc


def run_build_analysis_dataset_stage(
    *,
    input_csv: str,
    inference_csv: str,
    analysis_csv: str,
    runs_dir: str,
    run_id: str | None,
    default_inference_csv: str,
    default_analysis_csv: str,
    sample_poems: int | None = None,
    sample_seed: int | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    manager = RunArtifactsManager(runs_dir)
    context = manager.prepare_run(run_id)
    run_inference_path = manager.artifact_path(context, INFERENCE_ARTIFACT)
    run_analysis_path = manager.artifact_path(context, ANALYSIS_ARTIFACT)
    effective_inference_path = _prefer_run_input_path(inference_csv, default_inference_csv, run_inference_path)
    effective_analysis_path = _effective_output_path(analysis_csv, default_analysis_csv, run_analysis_path, run_id)

    try:
        df = build_analysis_dataset(
            input_csv,
            effective_inference_path,
            effective_analysis_path,
            progress_callback=progress_callback,
            sample_poems=sample_poems,
            sample_seed=sample_seed,
        )
        manager.mirror_artifact(effective_analysis_path, run_analysis_path)
        manager.mirror_artifact(run_analysis_path, analysis_csv)
        manifest_path = manager.record_stage(
            context,
            "build_analysis_dataset",
            "ok",
            {
                "inputs": {
                    "input_csv": str(Path(input_csv)),
                    "inference_csv": str(Path(effective_inference_path)),
                },
                "outputs": {
                    "requested_analysis_csv": str(Path(analysis_csv)),
                    "run_analysis_csv": str(run_analysis_path),
                },
                "rows": int(len(df)),
                "sample_poems": sample_poems,
                "sample_seed": sample_seed,
            },
        )
        return {
            "action": "build-analysis-dataset",
            "rows": int(len(df)),
            "input": str(Path(input_csv)),
            "inference": str(Path(effective_inference_path)),
            "analysis_csv": str(Path(analysis_csv)),
            "run_id": context.run_id,
            "run_dir": str(context.run_dir),
            "artifacts": {
                "manifest_json": str(manifest_path),
                "analysis_csv": str(run_analysis_path),
            },
        }
    except Exception as exc:
        manifest_path = manager.record_stage(
            context,
            "build_analysis_dataset",
            "error",
            {
                "inputs": {
                    "input_csv": str(Path(input_csv)),
                    "inference_csv": str(Path(effective_inference_path)),
                },
                "outputs": {
                    "requested_analysis_csv": str(Path(analysis_csv)),
                    "run_analysis_csv": str(run_analysis_path),
                },
                "sample_poems": sample_poems,
                "sample_seed": sample_seed,
                "error": str(exc),
            },
        )
        raise RuntimeError(
            f"Build-analysis-dataset stage failed. Run: {context.run_id}. Manifest: {manifest_path}. Error: {exc}"
        ) from exc


def run_stats_stage(
    *,
    input_csv: str,
    inference_csv: str,
    analysis_csv: str,
    output_json: str,
    report_md: str | None,
    runs_dir: str,
    run_id: str | None,
    default_inference_csv: str,
    default_analysis_csv: str,
    default_output_json: str,
    sample_poems: int | None = None,
    sample_seed: int | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    manager = RunArtifactsManager(runs_dir)
    context = manager.prepare_run(run_id)
    run_inference_path = manager.artifact_path(context, INFERENCE_ARTIFACT)
    run_analysis_path = manager.artifact_path(context, ANALYSIS_ARTIFACT)
    run_json_path = manager.artifact_path(context, STATS_JSON_ARTIFACT)
    run_md_path = manager.artifact_path(context, STATS_MD_ARTIFACT)

    effective_inference_path = _prefer_run_input_path(inference_csv, default_inference_csv, run_inference_path)
    effective_analysis_path = _effective_output_path(analysis_csv, default_analysis_csv, run_analysis_path, run_id)
    effective_json_path = _effective_output_path(output_json, default_output_json, run_json_path, run_id)

    if report_md is None:
        requested_report_md = str(Path(output_json).with_suffix(".md"))
        default_report_md = str(Path(default_output_json).with_suffix(".md"))
    else:
        requested_report_md = report_md
        default_report_md = report_md
    effective_md_path = _effective_output_path(requested_report_md, default_report_md, run_md_path, run_id)

    def _stage_payload_base() -> dict[str, Any]:
        return {
            "inputs": {
                "input_csv": str(Path(input_csv)),
                "inference_csv": str(Path(effective_inference_path)),
            },
            "outputs": {
                "requested_analysis_csv": str(Path(analysis_csv)),
                "requested_output_json": str(Path(output_json)),
                "requested_report_md": str(Path(requested_report_md)),
                "run_analysis_csv": str(run_analysis_path),
                "run_output_json": str(run_json_path),
                "run_report_md": str(run_md_path),
            },
        }

    try:
        analysis_kwargs: dict[str, Any] = {
            "report_md": effective_md_path,
        }
        if sample_poems is not None:
            analysis_kwargs["sample_poems"] = sample_poems
        if sample_seed is not None:
            analysis_kwargs["sample_seed"] = sample_seed
        if progress_callback is not None:
            analysis_kwargs["progress_callback"] = progress_callback

        results = run_all_analyses(
            input_csv,
            effective_inference_path,
            effective_json_path,
            effective_analysis_path,
            **analysis_kwargs,
        )
    except Exception as exc:
        stage_payload = _stage_payload_base()
        stage_payload["error"] = str(exc)
        for source, destination in (
            (effective_analysis_path, run_analysis_path),
            (effective_json_path, run_json_path),
            (effective_md_path, run_md_path),
            (run_analysis_path, analysis_csv),
            (run_json_path, output_json),
            (run_md_path, requested_report_md),
        ):
            path = Path(source)
            if path.exists():
                manager.mirror_artifact(source, destination)
        manifest_path = manager.record_stage(context, "stats", "error", stage_payload)
        raise RuntimeError(
            f"Stats stage failed. Run: {context.run_id}. Manifest: {manifest_path}. Error: {exc}"
        ) from exc

    manager.mirror_artifact(effective_analysis_path, run_analysis_path)
    manager.mirror_artifact(effective_json_path, run_json_path)
    manager.mirror_artifact(effective_md_path, run_md_path)
    manager.mirror_artifact(run_analysis_path, analysis_csv)
    manager.mirror_artifact(run_json_path, output_json)
    manager.mirror_artifact(run_md_path, requested_report_md)

    manifest_path = manager.record_stage(
        context,
        "stats",
        "ok",
        {
            **_stage_payload_base(),
            "sections": list(results.keys()),
            "sample_poems": sample_poems,
            "sample_seed": sample_seed,
        },
    )
    return {
        "action": "stats",
        "input": str(Path(input_csv)),
        "inference": str(Path(effective_inference_path)),
        "analysis_csv": str(Path(analysis_csv)),
        "output_json": str(Path(output_json)),
        "report_md": str(Path(requested_report_md)),
        "sections": list(results.keys()),
        "run_id": context.run_id,
        "run_dir": str(context.run_dir),
        "artifacts": {
            "manifest_json": str(manifest_path),
            "analysis_csv": str(run_analysis_path),
            "output_json": str(run_json_path),
            "report_md": str(run_md_path),
        },
    }

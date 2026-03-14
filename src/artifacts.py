from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sanitize_run_id(run_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", run_id.strip())
    cleaned = cleaned.strip("-.")
    if not cleaned:
        raise ValueError("Run ID must contain at least one alphanumeric character")
    return cleaned


def generate_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"run-{timestamp}-{uuid4().hex[:8]}"


def _atomic_write_bytes(path: str | Path, payload: bytes) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_file: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            delete=False,
            dir=str(output_path.parent),
            prefix=f".{output_path.name}.",
            suffix=".tmp",
        ) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            tmp_file = handle.name
        os.replace(tmp_file, output_path)
        return output_path
    finally:
        if tmp_file and os.path.exists(tmp_file):
            os.remove(tmp_file)


def atomic_write_text(path: str | Path, text: str, encoding: str = "utf-8") -> Path:
    return _atomic_write_bytes(path, text.encode(encoding))


def atomic_write_json(path: str | Path, payload: dict[str, Any]) -> Path:
    return atomic_write_text(path, json.dumps(payload, indent=2))


def atomic_copy_file(source_path: str | Path, destination_path: str | Path) -> Path:
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Cannot copy missing artifact: {source}")
    return _atomic_write_bytes(destination_path, source.read_bytes())


@dataclass(frozen=True)
class RunContext:
    run_id: str
    runs_dir: Path
    run_dir: Path


class RunArtifactsManager:
    def __init__(self, runs_dir: str | Path) -> None:
        resolved = Path(runs_dir).expanduser()
        self.runs_dir = resolved.resolve() if resolved.is_absolute() else resolved

    def prepare_run(self, run_id: str | None = None) -> RunContext:
        resolved_id = _sanitize_run_id(run_id) if run_id else generate_run_id()
        run_dir = self.runs_dir / resolved_id
        run_dir.mkdir(parents=True, exist_ok=True)
        context = RunContext(run_id=resolved_id, runs_dir=self.runs_dir, run_dir=run_dir)
        self._ensure_manifest(context)
        self._write_latest_pointer(context)
        return context

    def artifact_path(self, context: RunContext, filename: str) -> Path:
        return context.run_dir / filename

    def mirror_artifact(self, source_path: str | Path, destination_path: str | Path) -> Path:
        source = Path(source_path)
        destination = Path(destination_path)
        if self._same_path(source, destination):
            return destination
        return atomic_copy_file(source, destination)

    def record_stage(self, context: RunContext, stage_name: str, status: str, details: dict[str, Any]) -> Path:
        manifest = self._read_manifest(context)
        now = _utc_now_iso()
        manifest["updated_at"] = now
        manifest.setdefault("stages", {})
        manifest["stages"][stage_name] = {"status": status, "updated_at": now, **details}
        manifest_path = self._manifest_path(context)
        atomic_write_json(manifest_path, manifest)
        self._write_latest_pointer(context, manifest)
        return manifest_path

    def _manifest_path(self, context: RunContext) -> Path:
        return context.run_dir / "manifest.json"

    def _ensure_manifest(self, context: RunContext) -> None:
        manifest_path = self._manifest_path(context)
        if manifest_path.exists():
            return
        now = _utc_now_iso()
        base_manifest = {
            "run_id": context.run_id,
            "run_dir": str(context.run_dir.resolve()),
            "created_at": now,
            "updated_at": now,
            "stages": {},
        }
        atomic_write_json(manifest_path, base_manifest)

    def _read_manifest(self, context: RunContext) -> dict[str, Any]:
        manifest_path = self._manifest_path(context)
        if not manifest_path.exists():
            self._ensure_manifest(context)
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def _write_latest_pointer(self, context: RunContext, manifest: dict[str, Any] | None = None) -> None:
        payload_manifest = manifest if manifest is not None else self._read_manifest(context)
        stage_statuses = {
            stage_name: stage_data.get("status")
            for stage_name, stage_data in payload_manifest.get("stages", {}).items()
            if isinstance(stage_data, dict)
        }
        pointer = {
            "run_id": context.run_id,
            "run_dir": str(context.run_dir.resolve()),
            "updated_at": payload_manifest.get("updated_at", _utc_now_iso()),
            "stage_statuses": stage_statuses,
        }
        pointer_path = self.runs_dir / "latest_run.json"
        atomic_write_json(pointer_path, pointer)

    @staticmethod
    def _same_path(left: Path, right: Path) -> bool:
        try:
            return left.resolve() == right.resolve()
        except FileNotFoundError:
            return left.absolute() == right.absolute()

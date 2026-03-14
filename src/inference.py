from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import inspect
import json
import os
import re
import threading
import unicodedata
from pathlib import Path
from typing import Any, Callable

import pandas as pd
from pydantic import BaseModel, Field

from .data_parser import (
    STATUS_COMPLETED,
    STATUS_SKIPPED_PRIOR_KNOWLEDGE,
    default_inference_dataframe,
    load_inference_dataset,
    load_input_dataset,
    serialize_json_columns,
)
from .logger import get_logger
from .utility import run_model
from .artifacts import atomic_write_json

logger = get_logger(__name__)

LITERARY_DEVICES = [
    "metaphor",
    "simile",
    "personification",
    "symbolism",
    "imagery",
    "allusion",
    "apostrophe",
    "hyperbole",
    "understatement",
    "irony",
    "paradox",
    "oxymoron",
    "metonymy",
    "synecdoche",
    "allegory",
    "alliteration",
    "assonance",
    "consonance",
    "rhyme",
    "internal rhyme",
    "onomatopoeia",
    "euphony",
    "cacophony",
    "repetition",
    "anaphora",
    "epistrophe",
    "parallelism",
    "enjambment",
    "caesura",
    "refrain",
    "meter",
    "rhythm",
    "stanza",
    "lineation",
    "juxtaposition",
]


class LiteraryDevicesInference(BaseModel):
    literary_devices: list[str] = Field(..., description="A list of literary devices identified in the poem.")


class ScoreInference(BaseModel):
    technical_craft_score: int = Field(..., ge=1, le=10)
    structure_score: int = Field(..., ge=1, le=10)
    diction_score: int = Field(..., ge=1, le=10)
    originality_score: int = Field(..., ge=1, le=10)
    impact_score: int = Field(..., ge=1, le=10)


class CheckPriorKnowledgeInference(BaseModel):
    author_name: str = Field(..., description="The full name of the author of the poem.")

STATUS_FAILED_MODEL_INFERENCE = "failed_model_inference"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STAGE_CACHE_PATH = PROJECT_ROOT / "data" / "cache" / "inference_stage_cache.json"


def _read_stage_cache_path() -> Path:
    override = os.getenv("INFERENCE_STAGE_CACHE_PATH", "").strip()
    if override:
        return Path(override).expanduser()
    return DEFAULT_STAGE_CACHE_PATH


def _compute_input_fingerprint(csv_file_path: str) -> str:
    path = Path(csv_file_path).expanduser().resolve()
    digest = hashlib.sha256()
    digest.update(str(path).encode("utf-8"))
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _poem_cache_key(poem_id: str, input_fingerprint: str) -> str:
    return f"{input_fingerprint}:{poem_id}"


class _InferenceStageCache:
    _file_lock = threading.Lock()

    def __init__(self, input_fingerprint: str, cache_path: Path | None = None) -> None:
        self.input_fingerprint = input_fingerprint
        self.cache_path = cache_path or _read_stage_cache_path()
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with self._file_lock:
            payload = self._load_payload()
            bucket = payload.setdefault(input_fingerprint, {})
            bucket.setdefault("prior", {})
            bucket.setdefault("literary_devices", {})
            bucket.setdefault("score", {})
            self._payload = payload

    def _load_payload(self) -> dict[str, Any]:
        if not self.cache_path.exists():
            return {}
        try:
            parsed = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def _persist(self) -> None:
        atomic_write_json(self.cache_path, self._payload)

    def _entry_key(self, poem_id: str, model: str) -> str:
        return f"{poem_id}::{model}"

    def get_prior(self, poem_id: str, model: str) -> bool | None:
        key = self._entry_key(poem_id, model)
        with self._file_lock:
            value = self._payload.get(self.input_fingerprint, {}).get("prior", {}).get(key)
        return bool(value) if isinstance(value, bool) else None

    def set_prior(self, poem_id: str, model: str, detected: bool) -> None:
        key = self._entry_key(poem_id, model)
        with self._file_lock:
            self._payload[self.input_fingerprint]["prior"][key] = bool(detected)
            self._persist()

    def get_literary_devices(self, poem_id: str, model: str) -> list[str] | None:
        key = self._entry_key(poem_id, model)
        with self._file_lock:
            value = self._payload.get(self.input_fingerprint, {}).get("literary_devices", {}).get(key)
        if not isinstance(value, list):
            return None
        return [str(item) for item in value]

    def set_literary_devices(self, poem_id: str, model: str, devices: list[str]) -> None:
        key = self._entry_key(poem_id, model)
        with self._file_lock:
            self._payload[self.input_fingerprint]["literary_devices"][key] = [str(item) for item in devices]
            self._persist()

    def get_score(self, poem_id: str, model: str) -> dict[str, int] | None:
        key = self._entry_key(poem_id, model)
        with self._file_lock:
            value = self._payload.get(self.input_fingerprint, {}).get("score", {}).get(key)
        if not isinstance(value, dict):
            return None
        required = {
            "technical_craft_score",
            "structure_score",
            "diction_score",
            "originality_score",
            "impact_score",
        }
        if not required.issubset(value):
            return None
        try:
            return {name: int(value[name]) for name in required}
        except Exception:
            return None

    def set_score(self, poem_id: str, model: str, score_payload: dict[str, Any]) -> None:
        key = self._entry_key(poem_id, model)
        cleaned = {
            "technical_craft_score": int(score_payload["technical_craft_score"]),
            "structure_score": int(score_payload["structure_score"]),
            "diction_score": int(score_payload["diction_score"]),
            "originality_score": int(score_payload["originality_score"]),
            "impact_score": int(score_payload["impact_score"]),
        }
        with self._file_lock:
            self._payload[self.input_fingerprint]["score"][key] = cleaned
            self._persist()


def _prior_knowledge_timeout_seconds(model: str) -> float:
    model_lower = model.lower()
    if "qwen" in model_lower:
        return 20.0
    if "deepseek" in model_lower:
        return 25.0
    return 25.0


def _inference_timeout_seconds(model: str) -> float:
    model_lower = model.lower()
    if "qwen" in model_lower:
        return 40.0
    if "deepseek" in model_lower:
        return 45.0
    return 30.0


def _normalize_name_tokens(name: str) -> list[str]:
    if not isinstance(name, str):
        return []
    normalized = unicodedata.normalize("NFKD", name)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower().strip()
    normalized = re.sub(r"[^a-z\s]", " ", normalized)
    ignore_tokens = {"mr", "mrs", "ms", "dr", "prof", "sir", "lady", "jr", "sr", "ii", "iii", "iv", "v"}
    return [token for token in normalized.split() if token and token not in ignore_tokens]



def _looks_like_unknown_author_guess(name: str) -> bool:
    if not isinstance(name, str):
        return True
    normalized = re.sub(r"[^a-z\s]", " ", name.lower()).strip()
    unknown_markers = {
        "i dont know",
        "i do not know",
        "dont know",
        "do not know",
        "unknown",
        "not sure",
        "no idea",
        "cannot say",
        "cant say",
    }
    return any(marker in normalized for marker in unknown_markers)



def _author_names_match_lenient(predicted_name: str, expected_name: str) -> bool:
    if _looks_like_unknown_author_guess(predicted_name):
        return False
    predicted_tokens = _normalize_name_tokens(predicted_name)
    expected_tokens = _normalize_name_tokens(expected_name)
    if not predicted_tokens or not expected_tokens:
        return False
    if predicted_tokens == expected_tokens or set(predicted_tokens) == set(expected_tokens):
        return True
    if len(predicted_tokens) == 1 or len(expected_tokens) == 1:
        return predicted_tokens == expected_tokens
    predicted_first, predicted_last = predicted_tokens[0], predicted_tokens[-1]
    expected_first, expected_last = expected_tokens[0], expected_tokens[-1]
    first_matches = predicted_first == expected_first or predicted_first[0] == expected_first[0]
    last_matches = predicted_last == expected_last
    if first_matches and last_matches:
        return True
    token_overlap = len(set(predicted_tokens) & set(expected_tokens))
    return last_matches and token_overlap >= 2



def load_poems_from_csv(file_path: str) -> pd.DataFrame:
    return load_input_dataset(file_path)



def validate_literary_devices_inference(list_of_devices: list[str]) -> list[str]:
    valid_devices = []
    seen = set()
    for device in list_of_devices:
        normalized_device = str(device).strip().lower()
        if normalized_device in LITERARY_DEVICES and normalized_device not in seen:
            valid_devices.append(normalized_device)
            seen.add(normalized_device)
    return valid_devices



def _build_prior_knowledge_prompt(poem_text: str) -> str:
    return (
        f"Here is a poem:\n\n{poem_text}\n\n"
        "Who is the author of this poem? If you do not know, write \"I don't know\". "
        "If you have a guess, provide the name of the author."
    )



def _build_literary_devices_prompt(poem_text: str) -> str:
    return (
        "You are a literary critic analyzing a poem. The poem is as follows:\n\n"
        f"{poem_text}\n\n"
        "Return the literary devices used in the poem in the `literary_devices` field. "
        "Choose devices only from this list: "
        f"{', '.join(LITERARY_DEVICES)}."
    )



def _build_score_prompt(poem_text: str) -> str:
    return (
        "You are a literary critic analyzing a poem. The poem is as follows:\n\n"
        f"{poem_text}\n\n"
        "Evaluate the poem on technical craft, structure, diction, originality, and impact. "
        "Assign each score from 1 to 10. "
        "Use 1-3 for weak, 4-6 for average, 7-8 for strong, and 9-10 for exceptional."
    )



def check_prior_knowledge(
    poem_dict: dict,
    model: str,
    input_fingerprint: str | None = None,
    stage_cache: _InferenceStageCache | None = None,
) -> bool:
    if input_fingerprint is None:
        input_fingerprint = "adhoc"
    poem_id = str(poem_dict.get("poem_id", ""))
    if stage_cache is not None:
        cached = stage_cache.get_prior(poem_id, model)
        if cached is not None:
            return cached

    prompt = _build_prior_knowledge_prompt(str(poem_dict.get("poem_text", "")))
    try:
        inference_result = run_model(
            prompt,
            CheckPriorKnowledgeInference,
            model,
            temperature=0.0,
            max_tokens=None,
            disable_retries=False,
            timeout_seconds=_prior_knowledge_timeout_seconds(model),
        )
    except Exception as exc:
        logger.warning(
            "Prior-knowledge check failed for poem_id=%s model=%s: %s. Treating as no prior-knowledge detection.",
            poem_id,
            model,
            exc,
        )
        if stage_cache is not None:
            stage_cache.set_prior(poem_id, model, False)
        return False
    detected = _author_names_match_lenient(inference_result["author_name"], poem_dict.get("author_name"))
    if stage_cache is not None:
        stage_cache.set_prior(poem_id, model, detected)
    return detected



def _base_result_fields(poem_dict: dict, input_fingerprint: str) -> dict:
    poem_id = str(poem_dict.get("poem_id"))
    return {
        "poem_id": poem_id,
        "source_input_fingerprint": input_fingerprint,
        "input_poem_cache_key": _poem_cache_key(poem_id, input_fingerprint),
        "poem_fetch_url": poem_dict.get("poem_fetch_url", ""),
        "poem_genre": poem_dict.get("poem_genre", ""),
        "year_of_publish": poem_dict.get("year_of_publish", ""),
        "author_name": poem_dict.get("author_name", ""),
        "author_age": poem_dict.get("author_age", ""),
        "author_gender": poem_dict.get("author_gender", ""),
        "author_ethnicity": poem_dict.get("author_ethnicity", ""),
        "author_nationality": poem_dict.get("author_nationality", ""),
    }



def run_single_inference(
    poem_dict: dict,
    model: str,
    input_fingerprint: str | None = None,
    stage_cache: _InferenceStageCache | None = None,
) -> dict:
    if input_fingerprint is None:
        input_fingerprint = "adhoc"
    poem_id = poem_dict.get("poem_id", "?")
    poem_text = str(poem_dict.get("poem_text", ""))
    timeout_seconds = _inference_timeout_seconds(model)
    logger.info("Scoring poem_id=%s with model=%s", poem_id, model)
    cached_literary_devices = stage_cache.get_literary_devices(str(poem_id), model) if stage_cache is not None else None
    if cached_literary_devices is None:
        prompt_literary_devices = _build_literary_devices_prompt(poem_text)
        literary_devices_inference = run_model(
            prompt_literary_devices,
            LiteraryDevicesInference,
            model,
            temperature=0.0,
            max_tokens=None,
            disable_retries=False,
            timeout_seconds=timeout_seconds,
        )
        literary_devices = validate_literary_devices_inference(literary_devices_inference["literary_devices"])
        if stage_cache is not None:
            stage_cache.set_literary_devices(str(poem_id), model, literary_devices)
    else:
        literary_devices = validate_literary_devices_inference(cached_literary_devices)
    logger.debug(
        "poem_id=%s model=%s literary_devices=%s",
        poem_id, model, literary_devices,
    )
    score_inference = stage_cache.get_score(str(poem_id), model) if stage_cache is not None else None
    if score_inference is None:
        prompt_score = _build_score_prompt(poem_text)
        score_inference = run_model(
            prompt_score,
            ScoreInference,
            model,
            temperature=0.0,
            max_tokens=None,
            disable_retries=False,
            timeout_seconds=timeout_seconds,
        )
        if stage_cache is not None:
            stage_cache.set_score(str(poem_id), model, score_inference)
    aggregate_score = sum(
        [
            score_inference["technical_craft_score"],
            score_inference["structure_score"],
            score_inference["diction_score"],
            score_inference["originality_score"],
            score_inference["impact_score"],
        ]
    )
    return {
        **_base_result_fields(poem_dict, input_fingerprint),
        "model": model,
        "status": STATUS_COMPLETED,
        "skip_reason": "",
        "prior_knowledge_detected_models": [],
        "literary_devices": literary_devices,
        "technical_craft_score": score_inference["technical_craft_score"],
        "structure_score": score_inference["structure_score"],
        "diction_score": score_inference["diction_score"],
        "originality_score": score_inference["originality_score"],
        "impact_score": score_inference["impact_score"],
        "aggregate_score": aggregate_score,
    }



def _build_skip_record(poem_dict: dict, detected_models: list[str], input_fingerprint: str) -> dict:
    return {
        **_base_result_fields(poem_dict, input_fingerprint),
        "model": "screening",
        "status": STATUS_SKIPPED_PRIOR_KNOWLEDGE,
        "skip_reason": "prior_knowledge_detected",
        "prior_knowledge_detected_models": detected_models,
        "literary_devices": [],
        "technical_craft_score": pd.NA,
        "structure_score": pd.NA,
        "diction_score": pd.NA,
        "originality_score": pd.NA,
        "impact_score": pd.NA,
        "aggregate_score": pd.NA,
    }


def _build_failed_model_record(poem_dict: dict, model: str, exc: Exception, input_fingerprint: str) -> dict:
    return {
        **_base_result_fields(poem_dict, input_fingerprint),
        "model": model,
        "status": STATUS_FAILED_MODEL_INFERENCE,
        "skip_reason": f"model_inference_error: {str(exc)}",
        "prior_knowledge_detected_models": [],
        "literary_devices": [],
        "technical_craft_score": pd.NA,
        "structure_score": pd.NA,
        "diction_score": pd.NA,
        "originality_score": pd.NA,
        "impact_score": pd.NA,
        "aggregate_score": pd.NA,
    }



def _scoped_rows(df: pd.DataFrame, input_fingerprint: str) -> pd.DataFrame:
    if df.empty:
        return df
    if "source_input_fingerprint" in df.columns:
        source_fingerprint = df["source_input_fingerprint"].fillna("").astype(str)
        scoped = df[source_fingerprint == input_fingerprint]
        if not scoped.empty:
            return scoped
        legacy_mask = source_fingerprint == ""
        if "input_poem_cache_key" in df.columns:
            cache_keys = df["input_poem_cache_key"].fillna("").astype(str)
            legacy_mask = legacy_mask & ((cache_keys == "") | (~cache_keys.str.contains(":")))
        return df[legacy_mask]
    if "input_poem_cache_key" in df.columns:
        prefix = f"{input_fingerprint}:"
        cache_keys = df["input_poem_cache_key"].fillna("").astype(str)
        scoped = df[cache_keys.str.startswith(prefix)]
        if not scoped.empty:
            return scoped
        return df[(cache_keys == "") | (~cache_keys.str.contains(":"))]
    return df


def _completed_pairs(df: pd.DataFrame, input_fingerprint: str) -> set[tuple[str, str]]:
    if df.empty:
        return set()
    scoped = _scoped_rows(df, input_fingerprint)
    completed = scoped[scoped["status"] == STATUS_COMPLETED]
    keys: set[tuple[str, str]] = set()
    for row in completed.itertuples():
        cache_key = str(getattr(row, "input_poem_cache_key", "") or _poem_cache_key(str(row.poem_id), input_fingerprint))
        keys.add((cache_key, str(row.model)))
    return keys



def _skipped_poems(df: pd.DataFrame, input_fingerprint: str) -> set[str]:
    if df.empty:
        return set()
    scoped = _scoped_rows(df, input_fingerprint)
    skipped = scoped[scoped["status"] == STATUS_SKIPPED_PRIOR_KNOWLEDGE]
    keys = skipped["input_poem_cache_key"].fillna("").astype(str).tolist() if "input_poem_cache_key" in skipped.columns else []
    return {key for key in keys if key}



def _deduplicate_output(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return default_inference_dataframe()
    df = df.copy()
    df["poem_id"] = df["poem_id"].astype(str)
    df["model"] = df["model"].astype(str)
    if "source_input_fingerprint" not in df.columns:
        df["source_input_fingerprint"] = ""
    if "input_poem_cache_key" not in df.columns:
        df["input_poem_cache_key"] = ""
    screening = df[df["status"] == STATUS_SKIPPED_PRIOR_KNOWLEDGE].drop_duplicates(
        subset=["source_input_fingerprint", "poem_id", "status"],
        keep="last",
    )
    completed = df[df["status"] == STATUS_COMPLETED].drop_duplicates(
        subset=["source_input_fingerprint", "poem_id", "model", "status"],
        keep="last",
    )
    other = df[~df["status"].isin([STATUS_COMPLETED, STATUS_SKIPPED_PRIOR_KNOWLEDGE])]
    combined = pd.concat([completed, screening, other], ignore_index=True)
    return combined.sort_values(["poem_id", "status", "model"], kind="stable").reset_index(drop=True)


def _emit_progress_event(
    progress_callback: Callable[[dict[str, Any]], None] | None,
    payload: dict[str, Any],
) -> None:
    if progress_callback is None:
        return
    try:
        progress_callback(payload)
    except Exception:
        return


def _resolve_worker_count(max_workers: int | None, model_count: int) -> int:
    if model_count <= 1:
        return 1
    if max_workers is None:
        return min(8, model_count)
    return max(1, min(int(max_workers), model_count))


def _detect_prior_knowledge_models(
    poem_dict: dict,
    models: list[str],
    worker_count: int,
    input_fingerprint: str,
    stage_cache: _InferenceStageCache,
) -> list[str]:
    prior_signature = inspect.signature(check_prior_knowledge)
    use_cache_aware_check = len(prior_signature.parameters) >= 4

    def _invoke_prior_check(model: str) -> bool:
        if use_cache_aware_check:
            return check_prior_knowledge(poem_dict, model, input_fingerprint, stage_cache)
        return check_prior_knowledge(poem_dict, model)

    if worker_count <= 1 or len(models) <= 1:
        detected: list[str] = []
        for model in models:
            try:
                if _invoke_prior_check(model):
                    detected.append(model)
            except Exception as exc:
                logger.warning(
                    "Prior-knowledge screening error for poem_id=%s model=%s: %s",
                    poem_dict.get("poem_id", "?"),
                    model,
                    exc,
                )
        return detected

    detected: list[str] = []
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(_invoke_prior_check, model): model
            for model in models
        }
        for future in as_completed(futures):
            model = futures[future]
            try:
                if future.result():
                    detected.append(model)
            except Exception as exc:
                logger.warning(
                    "Prior-knowledge screening error for poem_id=%s model=%s: %s",
                    poem_dict.get("poem_id", "?"),
                    model,
                    exc,
                )
    return detected



def run_inference_on_dataset(
    csv_file_path: str,
    output_path: str,
    models: list[str],
    check_cache: bool = True,
    max_rows: int | None = None,
    max_workers: int | None = None,
    sample_size: int | None = None,
    sample_seed: int | None = None,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> pd.DataFrame:
    input_fingerprint = _compute_input_fingerprint(csv_file_path)
    stage_cache = _InferenceStageCache(input_fingerprint)
    poems_df = load_poems_from_csv(csv_file_path)
    if sample_size is not None and sample_size > 0 and sample_size < len(poems_df):
        poems_df = poems_df.sample(n=sample_size, random_state=sample_seed).sort_index(kind="stable")
        logger.info("sample_size=%d: sampled %d poems using seed=%s", sample_size, len(poems_df), sample_seed)
    poems = [row.to_dict() for _, row in poems_df.iterrows()]
    if max_rows is not None and max_rows > 0:
        poems = poems[:max_rows]
        logger.info("max_rows=%d: using first %d of %d poems", max_rows, len(poems), len(poems_df))
    worker_count = _resolve_worker_count(max_workers, len(models))
    logger.info("inference worker_count=%d for %d models", worker_count, len(models))
    output_file = Path(output_path)
    existing_df = load_inference_dataset(output_file) if check_cache else default_inference_dataframe()
    completed_pairs = _completed_pairs(existing_df, input_fingerprint)
    skipped_poems = _skipped_poems(existing_df, input_fingerprint)
    scoped_existing_df = _scoped_rows(existing_df, input_fingerprint)
    existing_poem_ids: set[str] = set()
    if not scoped_existing_df.empty:
        for row in scoped_existing_df.itertuples():
            cache_key = str(getattr(row, "input_poem_cache_key", "") or _poem_cache_key(str(row.poem_id), input_fingerprint))
            existing_poem_ids.add(cache_key)

    pending_model_tasks = 0
    pending_screenings = 0
    for poem_dict in poems:
        poem_id = str(poem_dict.get("poem_id"))
        poem_cache_key = _poem_cache_key(poem_id, input_fingerprint)
        if poem_cache_key in skipped_poems:
            continue
        missing_models = [model for model in models if (poem_cache_key, model) not in completed_pairs]
        if not missing_models:
            continue
        pending_model_tasks += len(missing_models)
        if poem_cache_key not in existing_poem_ids:
            pending_screenings += 1

    total_units = pending_model_tasks + pending_screenings + 1
    completed_units = 0
    completed_model_tasks = 0
    completed_screenings = 0
    _emit_progress_event(
        progress_callback,
        {
            "event": "start",
            "total_poems": len(poems),
            "total_models": len(models),
            "max_workers": worker_count,
            "pending_model_tasks": pending_model_tasks,
            "pending_screenings": pending_screenings,
            "total_units": total_units,
            "completed_units": completed_units,
        },
    )

    new_rows: list[dict] = []
    inference_signature = inspect.signature(run_single_inference)
    use_cache_aware_inference = len(inference_signature.parameters) >= 4

    def _invoke_single_inference(poem_dict: dict, model: str) -> dict:
        if use_cache_aware_inference:
            return run_single_inference(poem_dict, model, input_fingerprint, stage_cache)
        return run_single_inference(poem_dict, model)

    try:
        for poem_index, poem_dict in enumerate(poems, start=1):
            poem_id = str(poem_dict.get("poem_id"))
            poem_cache_key = _poem_cache_key(poem_id, input_fingerprint)
            _emit_progress_event(
                progress_callback,
                {
                    "event": "poem_start",
                    "poem_id": poem_id,
                    "poem_index": poem_index,
                    "total_poems": len(poems),
                    "completed_units": completed_units,
                    "total_units": total_units,
                },
            )

            if poem_cache_key in skipped_poems:
                _emit_progress_event(
                    progress_callback,
                    {
                        "event": "poem_cached_skip",
                        "poem_id": poem_id,
                        "completed_units": completed_units,
                        "total_units": total_units,
                    },
                )
                continue
            missing_models = [model for model in models if (poem_cache_key, model) not in completed_pairs]
            if not missing_models:
                _emit_progress_event(
                    progress_callback,
                    {
                        "event": "poem_cached_complete",
                        "poem_id": poem_id,
                        "completed_units": completed_units,
                        "total_units": total_units,
                    },
                )
                continue

            if poem_cache_key not in existing_poem_ids:
                _emit_progress_event(
                    progress_callback,
                    {
                        "event": "screening_start",
                        "poem_id": poem_id,
                        "completed_units": completed_units,
                        "total_units": total_units,
                    },
                )
                detected_models = _detect_prior_knowledge_models(
                    poem_dict,
                    models,
                    worker_count,
                    input_fingerprint,
                    stage_cache,
                )
                completed_screenings += 1
                completed_units += 1
                _emit_progress_event(
                    progress_callback,
                    {
                        "event": "screening_complete",
                        "poem_id": poem_id,
                        "detected_models": list(detected_models),
                        "completed_screenings": completed_screenings,
                        "completed_units": completed_units,
                        "total_units": total_units,
                    },
                )
                if detected_models:
                    new_rows.append(_build_skip_record(poem_dict, detected_models, input_fingerprint))
                    skipped_poems.add(poem_cache_key)
                    _emit_progress_event(
                        progress_callback,
                        {
                            "event": "poem_skipped",
                            "poem_id": poem_id,
                            "detected_models": list(detected_models),
                            "completed_units": completed_units,
                            "total_units": total_units,
                        },
                    )
                    continue
            for model in missing_models:
                _emit_progress_event(
                    progress_callback,
                    {
                        "event": "model_start",
                        "poem_id": poem_id,
                        "model": model,
                        "completed_model_tasks": completed_model_tasks,
                        "completed_units": completed_units,
                        "total_units": total_units,
                    },
                )

            if worker_count <= 1 or len(missing_models) <= 1:
                for model in missing_models:
                    try:
                        result = _invoke_single_inference(poem_dict, model)
                    except Exception as exc:
                        logger.error(
                            "Inference failed for poem_id=%s model=%s: %s",
                            poem_id,
                            model,
                            exc,
                            exc_info=True,
                        )
                        result = _build_failed_model_record(poem_dict, model, exc, input_fingerprint)
                        _emit_progress_event(
                            progress_callback,
                            {
                                "event": "model_error",
                                "poem_id": poem_id,
                                "model": model,
                                "error": str(exc),
                                "completed_model_tasks": completed_model_tasks,
                                "completed_units": completed_units,
                                "total_units": total_units,
                            },
                        )
                    new_rows.append(result)
                    completed_pairs.add((poem_cache_key, model))
                    completed_model_tasks += 1
                    completed_units += 1
                    _emit_progress_event(
                        progress_callback,
                        {
                            "event": "model_complete",
                            "poem_id": poem_id,
                            "model": model,
                            "completed_model_tasks": completed_model_tasks,
                            "completed_units": completed_units,
                            "total_units": total_units,
                        },
                    )
            else:
                with ThreadPoolExecutor(max_workers=worker_count) as executor:
                    futures = {
                        executor.submit(_invoke_single_inference, poem_dict, model): model
                        for model in missing_models
                    }
                    for future in as_completed(futures):
                        model = futures[future]
                        try:
                            result = future.result()
                        except Exception as exc:
                            logger.error(
                                "Inference failed for poem_id=%s model=%s: %s",
                                poem_id,
                                model,
                                exc,
                                exc_info=True,
                            )
                            result = _build_failed_model_record(poem_dict, model, exc, input_fingerprint)
                            _emit_progress_event(
                                progress_callback,
                                {
                                    "event": "model_error",
                                    "poem_id": poem_id,
                                    "model": model,
                                    "error": str(exc),
                                    "completed_model_tasks": completed_model_tasks,
                                    "completed_units": completed_units,
                                    "total_units": total_units,
                                },
                            )
                        new_rows.append(result)
                        completed_pairs.add((poem_cache_key, model))
                        completed_model_tasks += 1
                        completed_units += 1
                        _emit_progress_event(
                            progress_callback,
                            {
                                "event": "model_complete",
                                "poem_id": poem_id,
                                "model": model,
                                "completed_model_tasks": completed_model_tasks,
                                "completed_units": completed_units,
                                "total_units": total_units,
                            },
                        )

        combined_df = _deduplicate_output(pd.concat([existing_df, pd.DataFrame(new_rows)], ignore_index=True))
        _emit_progress_event(
            progress_callback,
            {
                "event": "persist_start",
                "rows": int(len(combined_df)),
                "completed_units": completed_units,
                "total_units": total_units,
            },
        )
        output_file.parent.mkdir(parents=True, exist_ok=True)
        persisted_df = serialize_json_columns(combined_df, ["literary_devices", "prior_knowledge_detected_models"])
        tmp_output_file = Path(f"{output_file}.tmp")
        persisted_df.to_csv(tmp_output_file, index=False)
        tmp_output_file.replace(output_file)
        completed_units += 1
        _emit_progress_event(
            progress_callback,
            {
                "event": "persist_complete",
                "rows": int(len(combined_df)),
                "completed_units": completed_units,
                "total_units": total_units,
            },
        )
        _emit_progress_event(
            progress_callback,
            {
                "event": "complete",
                "rows": int(len(combined_df)),
                "new_rows": int(len(new_rows)),
                "completed_model_tasks": completed_model_tasks,
                "completed_screenings": completed_screenings,
                "completed_units": completed_units,
                "total_units": total_units,
            },
        )
        return combined_df
    except Exception as exc:
        _emit_progress_event(
            progress_callback,
            {
                "event": "error",
                "stage": "infer",
                "message": str(exc),
                "completed_model_tasks": completed_model_tasks,
                "completed_screenings": completed_screenings,
                "completed_units": completed_units,
                "total_units": total_units,
            },
        )
        raise

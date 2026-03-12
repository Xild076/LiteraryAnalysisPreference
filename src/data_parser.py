from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Iterable

import pandas as pd

INPUT_REQUIRED_COLUMNS = [
    "poem_id",
    "poem_text",
    "poem_fetch_url",
    "poem_genre",
    "year_of_publish",
    "author_name",
    "author_age",
    "author_gender",
    "author_ethnicity",
    "author_nationality",
]

INFERENCE_REQUIRED_COLUMNS = [
    "poem_id",
    "model",
    "status",
    "skip_reason",
    "prior_knowledge_detected_models",
    "poem_fetch_url",
    "poem_genre",
    "year_of_publish",
    "author_name",
    "author_age",
    "author_gender",
    "author_ethnicity",
    "author_nationality",
    "literary_devices_rationale",
    "literary_devices",
    "score_rationale",
    "technical_craft_score",
    "structure_score",
    "diction_score",
    "originality_score",
    "impact_score",
    "aggregate_score",
]

STATUS_COMPLETED = "completed"
STATUS_SKIPPED_PRIOR_KNOWLEDGE = "skipped_prior_knowledge"


def _strip_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(column).strip() for column in df.columns]
    return df


def _coerce_devices(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        for parser in (json.loads, ast.literal_eval):
            try:
                parsed = parser(text)
            except Exception:
                continue
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        return [text]
    return [str(value)]


def _coerce_detected_models(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        for parser in (json.loads, ast.literal_eval):
            try:
                parsed = parser(text)
            except Exception:
                continue
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        return [text]
    return [str(value)]


def default_inference_dataframe() -> pd.DataFrame:
    return pd.DataFrame(columns=INFERENCE_REQUIRED_COLUMNS)



def validate_required_columns(df: pd.DataFrame, kind: str) -> None:
    required = INPUT_REQUIRED_COLUMNS if kind == "input" else INFERENCE_REQUIRED_COLUMNS
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required {kind} columns: {', '.join(missing)}")



def load_input_dataset(path: str | Path) -> pd.DataFrame:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {file_path}")
    df = pd.read_csv(file_path)
    df = _strip_columns(df)
    validate_required_columns(df, "input")
    return df



def _normalize_inference_status(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "status" not in df.columns:
        if "model" in df.columns:
            model_series = df["model"].fillna("").astype(str).str.strip()
            skipped = model_series.isin(["", "N/A", "screening"])
            df["status"] = STATUS_COMPLETED
            df.loc[skipped, "status"] = STATUS_SKIPPED_PRIOR_KNOWLEDGE
        else:
            df["status"] = STATUS_COMPLETED
    if "skip_reason" not in df.columns:
        df["skip_reason"] = ""
        skipped_mask = df["status"] == STATUS_SKIPPED_PRIOR_KNOWLEDGE
        df.loc[skipped_mask, "skip_reason"] = "prior_knowledge_detected"
    if "prior_knowledge_detected_models" not in df.columns:
        df["prior_knowledge_detected_models"] = "[]"
    if "literary_devices" in df.columns:
        df["literary_devices"] = df["literary_devices"].apply(_coerce_devices)
    else:
        df["literary_devices"] = [[] for _ in range(len(df))]
    df["prior_knowledge_detected_models"] = df["prior_knowledge_detected_models"].apply(_coerce_detected_models)
    for column in INFERENCE_REQUIRED_COLUMNS:
        if column not in df.columns:
            if column in {"technical_craft_score", "structure_score", "diction_score", "originality_score", "impact_score", "aggregate_score"}:
                df[column] = pd.NA
            elif column in {"literary_devices", "prior_knowledge_detected_models"}:
                df[column] = [[] for _ in range(len(df))]
            else:
                df[column] = ""
    return df[INFERENCE_REQUIRED_COLUMNS]



def load_inference_dataset(path: str | Path) -> pd.DataFrame:
    file_path = Path(path)
    if not file_path.exists() or file_path.stat().st_size == 0:
        return default_inference_dataframe()
    df = pd.read_csv(file_path)
    df = _strip_columns(df)
    return _normalize_inference_status(df)



def serialize_json_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    df = df.copy()
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(json.dumps)
    return df

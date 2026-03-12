from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

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
from .utility import run_model

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
    rationale: str = Field(..., description="A detailed explanation of the literary devices used in the poem.")
    literary_devices: list[str] = Field(..., description="A list of literary devices identified in the poem.")


class ScoreInference(BaseModel):
    rationale: str = Field(..., description="A detailed explanation of the score.")
    technical_craft_score: int = Field(..., ge=1, le=10)
    structure_score: int = Field(..., ge=1, le=10)
    diction_score: int = Field(..., ge=1, le=10)
    originality_score: int = Field(..., ge=1, le=10)
    impact_score: int = Field(..., ge=1, le=10)


class CheckPriorKnowledgeInference(BaseModel):
    author_name: str = Field(..., description="The full name of the author of the poem.")



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



def check_prior_knowledge(poem_dict: dict, model: str) -> bool:
    prompt = (
        f"Here is a poem:\n\n{poem_dict.get('poem_text', '')}\n\n"
        "Who is the author of this poem? If you do not know, write \"I don't know\". "
        "If you have a guess, provide the name of the author."
    )
    inference_result = run_model(prompt, CheckPriorKnowledgeInference, model, temperature=0.0, max_tokens=120)
    return _author_names_match_lenient(inference_result["author_name"], poem_dict.get("author_name"))



def _base_result_fields(poem_dict: dict) -> dict:
    return {
        "poem_id": poem_dict.get("poem_id"),
        "poem_fetch_url": poem_dict.get("poem_fetch_url", ""),
        "poem_genre": poem_dict.get("poem_genre", ""),
        "year_of_publish": poem_dict.get("year_of_publish", ""),
        "author_name": poem_dict.get("author_name", ""),
        "author_age": poem_dict.get("author_age", ""),
        "author_gender": poem_dict.get("author_gender", ""),
        "author_ethnicity": poem_dict.get("author_ethnicity", ""),
        "author_nationality": poem_dict.get("author_nationality", ""),
    }



def run_single_inference(poem_dict: dict, model: str) -> dict:
    poem_text = poem_dict.get("poem_text", "")
    prompt_literary_devices = (
        "You are a literary critic analyzing a poem. The poem is as follows:\n\n"
        f"{poem_text}\n\n"
        "Identify the literary devices used in the poem. Provide a detailed rationale and a list of "
        "devices drawn only from this list: "
        f"{', '.join(LITERARY_DEVICES)}."
    )
    literary_devices_inference = run_model(prompt_literary_devices, LiteraryDevicesInference, model, temperature=0.2, max_tokens=500)
    literary_devices = validate_literary_devices_inference(literary_devices_inference["literary_devices"])
    prompt_score = (
        "You are a literary critic analyzing a poem. The poem is as follows:\n\n"
        f"{poem_text}\n\n"
        "Evaluate the poem on technical craft, structure, diction, originality, and impact. "
        "Provide a detailed rationale and assign each score from 1 to 10. "
        "Use 1-3 for weak, 4-6 for average, 7-8 for strong, and 9-10 for exceptional."
    )
    score_inference = run_model(prompt_score, ScoreInference, model, temperature=0.2, max_tokens=500)
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
        **_base_result_fields(poem_dict),
        "model": model,
        "status": STATUS_COMPLETED,
        "skip_reason": "",
        "prior_knowledge_detected_models": [],
        "literary_devices_rationale": literary_devices_inference["rationale"],
        "literary_devices": literary_devices,
        "score_rationale": score_inference["rationale"],
        "technical_craft_score": score_inference["technical_craft_score"],
        "structure_score": score_inference["structure_score"],
        "diction_score": score_inference["diction_score"],
        "originality_score": score_inference["originality_score"],
        "impact_score": score_inference["impact_score"],
        "aggregate_score": aggregate_score,
    }



def _build_skip_record(poem_dict: dict, detected_models: list[str]) -> dict:
    return {
        **_base_result_fields(poem_dict),
        "model": "screening",
        "status": STATUS_SKIPPED_PRIOR_KNOWLEDGE,
        "skip_reason": "prior_knowledge_detected",
        "prior_knowledge_detected_models": detected_models,
        "literary_devices_rationale": "",
        "literary_devices": [],
        "score_rationale": "",
        "technical_craft_score": pd.NA,
        "structure_score": pd.NA,
        "diction_score": pd.NA,
        "originality_score": pd.NA,
        "impact_score": pd.NA,
        "aggregate_score": pd.NA,
    }



def _completed_pairs(df: pd.DataFrame) -> set[tuple[str, str]]:
    if df.empty:
        return set()
    completed = df[df["status"] == STATUS_COMPLETED]
    return {(str(row.poem_id), str(row.model)) for row in completed.itertuples()}



def _skipped_poems(df: pd.DataFrame) -> set[str]:
    if df.empty:
        return set()
    skipped = df[df["status"] == STATUS_SKIPPED_PRIOR_KNOWLEDGE]
    return {str(poem_id) for poem_id in skipped["poem_id"].tolist()}



def _deduplicate_output(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return default_inference_dataframe()
    df = df.copy()
    df["poem_id"] = df["poem_id"].astype(str)
    df["model"] = df["model"].astype(str)
    screening = df[df["status"] == STATUS_SKIPPED_PRIOR_KNOWLEDGE].drop_duplicates(subset=["poem_id", "status"], keep="last")
    completed = df[df["status"] == STATUS_COMPLETED].drop_duplicates(subset=["poem_id", "model", "status"], keep="last")
    other = df[~df["status"].isin([STATUS_COMPLETED, STATUS_SKIPPED_PRIOR_KNOWLEDGE])]
    combined = pd.concat([completed, screening, other], ignore_index=True)
    return combined.sort_values(["poem_id", "status", "model"], kind="stable").reset_index(drop=True)



def run_inference_on_dataset(csv_file_path: str, output_path: str, models: list[str], check_cache: bool = True) -> pd.DataFrame:
    poems_df = load_poems_from_csv(csv_file_path)
    output_file = Path(output_path)
    existing_df = load_inference_dataset(output_file) if check_cache else default_inference_dataframe()
    completed_pairs = _completed_pairs(existing_df)
    skipped_poems = _skipped_poems(existing_df)
    new_rows: list[dict] = []
    for _, poem_row in poems_df.iterrows():
        poem_dict = poem_row.to_dict()
        poem_id = str(poem_dict.get("poem_id"))
        if poem_id in skipped_poems:
            continue
        missing_models = [model for model in models if (poem_id, model) not in completed_pairs]
        if not missing_models:
            continue
        existing_poem_rows = existing_df[existing_df["poem_id"].astype(str) == poem_id]
        if existing_poem_rows.empty:
            detected_models = [model for model in models if check_prior_knowledge(poem_dict, model)]
            if detected_models:
                new_rows.append(_build_skip_record(poem_dict, detected_models))
                skipped_poems.add(poem_id)
                continue
        for model in missing_models:
            result = run_single_inference(poem_dict, model)
            new_rows.append(result)
            completed_pairs.add((poem_id, model))
    combined_df = _deduplicate_output(pd.concat([existing_df, pd.DataFrame(new_rows)], ignore_index=True))
    output_file.parent.mkdir(parents=True, exist_ok=True)
    persisted_df = serialize_json_columns(combined_df, ["literary_devices", "prior_knowledge_detected_models"])
    persisted_df.to_csv(output_file, index=False)
    return combined_df

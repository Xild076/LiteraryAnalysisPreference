from pydantic import BaseModel, Field
import pandas as pd
from pathlib import Path

literary_devices = [
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
    "juxtaposition"
]

class LiteraryDevicesInference(BaseModel):
    rationale: str = Field(..., description="A detailed explanation of the literary devices used in the poem.")
    literary_devices: list[str] = Field(..., description="A list of literary devices identified in the poem (e.g., imagery, metaphor, sound devices, symbolism). Must be one of the devices specified in the list of literary devices provided in the prompt.")

class ScoreInference(BaseModel):
    rationale: str = Field(..., description="A detailed explanation of the score.")
    technical_craft_score: int = Field(..., ge=1, le=10, description="Score for technical craft (1-10). Evaluates the use and effectiveness of literary devices (imagery, metaphor, sound devices, symbolism).")
    structure_score: int = Field(..., ge=1, le=10, description="Score for structure (1-10). Evaluates the organization and progression of the poem (stanzas, pacing, coherence).")
    diction_score: int = Field(..., ge=1, le=10, description="Score for diction (1-10). Evaluates the quality and precision of language, word choice, and stylistic fluency.")
    originality_score: int = Field(..., ge=1, le=10, description="Score for originality (1-10). Evaluates the novelty of imagery, ideas, or perspective.")
    impact_score: int = Field(..., ge=1, le=10, description="Score for impact (1-10). Evaluates the poem’s ability to evoke feeling, reflection, or memorability.")

try:
    from utility import run_model
except ModuleNotFoundError:
    from src.utility import run_model

SUPPORTED_MODELS = [
    "gpt-5.4",
    "gpt-5.3",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite-preview",
]

DEFAULT_MODEL_LIST = ["gpt-5.4", "claude-opus-4-6", "gemini-3.1-pro-preview"]

OUTPUT_COLUMNS = [
    "poem_id",
    "model",
    "poem_text",
    "poem_fetch_url",
    "poem_genre",
    "author_name",
    "year_of_publish",
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
    "inference_error",
]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize header names so small formatting differences do not break lookups.
    df.columns = [str(col).strip().lstrip("\ufeff") for col in df.columns]
    return df


def _safe_value(row: pd.Series, key: str, default=""):
    value = row[key] if key in row.index else default
    if pd.isna(value):
        return default
    if isinstance(value, str):
        return value.strip()
    return value


def _default_literary_devices_output():
    return {
        "rationale": "N/A",
        "literary_devices": [],
    }


def _default_score_output():
    return {
        "rationale": "N/A",
        "technical_craft_score": 0,
        "structure_score": 0,
        "diction_score": 0,
        "originality_score": 0,
        "impact_score": 0,
        "aggregate_score": 0,
    }


def _prepare_input_df(input_file_name: str) -> pd.DataFrame:
    input_df = _normalize_columns(pd.read_csv(input_file_name))
    if "poem_text" not in input_df.columns:
        raise ValueError("Input CSV must include a 'poem_text' column")

    input_changed = False

    if "poem_id" not in input_df.columns:
        input_df.insert(0, "poem_id", range(1, len(input_df) + 1))
        input_changed = True
    else:
        poem_ids = input_df["poem_id"].astype("string").fillna("").str.strip()
        has_missing_ids = poem_ids.eq("").any()
        has_duplicate_ids = poem_ids.duplicated().any()

        if has_missing_ids or has_duplicate_ids:
            # Guarantee a one-to-one mapping between input rows and inference rows.
            input_df["poem_id"] = range(1, len(input_df) + 1)
            input_changed = True
        else:
            input_df["poem_id"] = poem_ids

    if input_changed:
        input_df.to_csv(input_file_name, index=False)
        print(f"Input CSV updated with stable poem_id values: {input_file_name}")

    return input_df


def _prepare_output_df(output_file_name: str, check_previous_inference: bool) -> pd.DataFrame:
    output_path = Path(output_file_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if check_previous_inference and output_path.exists():
        output_df = _normalize_columns(pd.read_csv(output_file_name))
    else:
        output_df = pd.DataFrame(columns=OUTPUT_COLUMNS)

    for col in OUTPUT_COLUMNS:
        if col not in output_df.columns:
            output_df[col] = ""

    return output_df


def _print_inference_result(poem_id, model, poem_text, literary_devices_output, score_output, inference_error):
    print(f"Poem ID: {poem_id}")
    print(f"Model: {model}")
    print(f"Poem: {poem_text}")
    print(f"Literary Devices Inference: {literary_devices_output}")
    print(f"Score Inference: {score_output}")
    if inference_error:
        print(f"Inference Error: {inference_error}")
    print("\n" + "=" * 50 + "\n")


def infer_literary_devices(poem_text, model: str = "gpt-5.4"):
    prompt = f"Analyze the following poem and identify the literary devices used. Provide a detailed rationale for your analysis.\n\nPoem:\n{poem_text}\n\nLiterary Devices to consider: {', '.join(literary_devices)}"
    output = run_model(prompt, LiteraryDevicesInference, model, temperature=0.0)
    
    # Validate literary devices:
    output["literary_devices"] = [device for device in output["literary_devices"] if device in literary_devices]

    return output

def infer_score(poem_text, model: str = "gpt-5.4"):
    prompt = f"Evaluate the following poem and provide a score from 1 to 10 for each of the following categories: technical craft, structure, diction, originality, and impact. 1-3 means weak, 4-6 average, 7-8 means fair, and 9-10 means exceptional.\n\nPoem:\n{poem_text}"
    output = run_model(prompt, ScoreInference, model, temperature=0.0)

    aggregate_score = (
        output["technical_craft_score"]
        + output["structure_score"]
        + output["diction_score"]
        + output["originality_score"]
        + output["impact_score"]
    )

    output["aggregate_score"] = aggregate_score

    return output

def inference_loop(
    input_file_name,
    output_file_name,
    model_list=None,
    check_previous_inference=False,
    immediate_saving=False,
    run_live_inference=False,
):
    if model_list is None:
        model_list = DEFAULT_MODEL_LIST

    unsupported_models = [model for model in model_list if model not in SUPPORTED_MODELS]
    if unsupported_models:
        raise ValueError(f"Unsupported model(s): {unsupported_models}. Supported models: {SUPPORTED_MODELS}")

    input_df = _prepare_input_df(input_file_name)
    output_df = _prepare_output_df(output_file_name, check_previous_inference)

    completed_pairs = set()
    if check_previous_inference and not output_df.empty and {"poem_id", "model"}.issubset(output_df.columns):
        completed_pairs = {
            (str(row["poem_id"]), str(row["model"]))
            for _, row in output_df[["poem_id", "model"]].dropna().iterrows()
        }

    for _, row in input_df.iterrows():
        poem_id = _safe_value(row, "poem_id", "")
        poem_text = _safe_value(row, "poem_text", "")

        for model in model_list:
            if check_previous_inference and (str(poem_id), model) in completed_pairs:
                continue

            inference_error = ""
            literary_devices_output = _default_literary_devices_output()
            score_output = _default_score_output()

            if run_live_inference:
                try:
                    literary_devices_output = infer_literary_devices(poem_text, model=model)
                    score_output = infer_score(poem_text, model=model)
                except Exception as exc:
                    inference_error = str(exc)

            _print_inference_result(
                poem_id,
                model,
                poem_text,
                literary_devices_output,
                score_output,
                inference_error,
            )

            output_row = {
                "poem_id": poem_id,
                "model": model,
                "poem_text": poem_text,
                "poem_fetch_url": _safe_value(row, "poem_fetch_url", ""),
                "poem_genre": _safe_value(row, "poem_genre", ""),
                "author_name": _safe_value(row, "author_name", ""),
                "year_of_publish": _safe_value(row, "year_of_publish", ""),
                "author_gender": _safe_value(row, "author_gender", ""),
                "author_ethnicity": _safe_value(row, "author_ethnicity", ""),
                "author_nationality": _safe_value(row, "author_nationality", ""),
                "literary_devices_rationale": literary_devices_output.get("rationale", "N/A"),
                "literary_devices": ", ".join(literary_devices_output.get("literary_devices", [])),
                "score_rationale": score_output.get("rationale", "N/A"),
                "technical_craft_score": score_output.get("technical_craft_score", 0),
                "structure_score": score_output.get("structure_score", 0),
                "diction_score": score_output.get("diction_score", 0),
                "originality_score": score_output.get("originality_score", 0),
                "impact_score": score_output.get("impact_score", 0),
                "aggregate_score": score_output.get("aggregate_score", 0),
                "inference_error": inference_error,
            }

            output_df = pd.concat([output_df, pd.DataFrame([output_row])], ignore_index=True)

            if check_previous_inference:
                completed_pairs.add((str(poem_id), model))

            if immediate_saving:
                output_df.to_csv(output_file_name, index=False)

    if not immediate_saving:
        output_df.to_csv(output_file_name, index=False)

    return output_df


if __name__ == "__main__":
    print(
        inference_loop(
            "data/poems.csv",
            "data/poems_inference_output.csv",
            ["gemini-3.1-pro-preview"],
            check_previous_inference=True,
            immediate_saving=True,
            run_live_inference=True,
        )
    )
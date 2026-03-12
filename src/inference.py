from pydantic import BaseModel, Field
import pandas as pd
from pathlib import Path

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

from utility import run_model

def load_poems_from_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df

def validate_literary_devices_inference(list_of_devices: list[str]):
    valid_devices = []
    for device in list_of_devices:
        if device in LITERARY_DEVICES:
            valid_devices.append(device)
    return valid_devices

def run_single_inference(poem_dict: dict, model: str) -> dict:
    poem_id = poem_dict.get("poem_id")
    poem_text = poem_dict.get("poem_text")
    poem_fetch_url = poem_dict.get("poem_fetch_url")
    poem_genre = poem_dict.get("poem_genre")
    year_of_publish = poem_dict.get("year_of_publish")
    author_name = poem_dict.get("author_name")
    author_age = poem_dict.get("author_age")
    author_gender = poem_dict.get("author_gender")
    author_ethnicity = poem_dict.get("author_ethnicity")
    author_nationality = poem_dict.get("author_nationality")

    prompt_literary_devices = f"""You are a literary critic analyzing a poem. The poem is as follows: \n\n{poem_text}\n\nIdentify the literary devices used in the poem. Provide a detailed rationale for your analysis and list the literary devices you identify, ensuring they are from the provided list of literary devices. The list of literary devices to choose from includes: {', '.join(LITERARY_DEVICES)}."""

    literary_devices_inference = run_model(prompt_literary_devices, LiteraryDevicesInference, model)
    literary_devices_inference["literary_devices"] = validate_literary_devices_inference(literary_devices_inference["literary_devices"])

    prompt_score = f"""You are a literary critic analyzing a poem. The poem is as follows: \n\n{poem_text}\n\nEvaluate the poem based on the following criteria: technical craft, structure, diction, originality, and impact. Provide a detailed rationale for your evaluation and assign a score from 1 to 10 for each criterion, where 1 is the lowest and 10 is the highest. 1-3 = weak, 4-6 = average, 7-8 = strong, 9-10 = exceptional."""

    score_inference = run_model(prompt_score, ScoreInference, model)
    aggregate_score = (score_inference["technical_craft_score"] + score_inference["structure_score"] + score_inference["diction_score"] + score_inference["originality_score"] + score_inference["impact_score"])

    return {
        "poem_id": poem_id,
        "poem_fetch_url": poem_fetch_url,
        "poem_genre": poem_genre,
        "year_of_publish": year_of_publish,
        "author_name": author_name,
        "author_age": author_age,
        "author_gender": author_gender,
        "author_ethnicity": author_ethnicity,
        "author_nationality": author_nationality,
        "literary_devices_rationale": literary_devices_inference["rationale"],
        "literary_devices": literary_devices_inference["literary_devices"],
        "score_rationale": score_inference["rationale"],
        "technical_craft_score": score_inference["technical_craft_score"],
        "structure_score": score_inference["structure_score"],
        "diction_score": score_inference["diction_score"],
        "originality_score": score_inference["originality_score"],
        "impact_score": score_inference["impact_score"],
        "aggregate_score": aggregate_score
    }


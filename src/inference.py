from pydantic import BaseModel, Field
from typing import Literal

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

from utility import run_model

def infer_literary_devices(poem_text, model=Literal["gpt-5.4", "gpt-5.3", "claude-opus-4-6", "claude-sonnet-4-6", "gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview"]):
    prompt = f"Analyze the following poem and identify the literary devices used. Provide a detailed rationale for your analysis.\n\nPoem:\n{poem_text}\n\nLiterary Devices to consider: {', '.join(literary_devices)}"
    output = run_model(prompt, LiteraryDevicesInference, model, temperature=0.0)
    
    # Validate literary devices:
    output['literary_devices'] = [device for device in output['literary_devices'] if device in literary_devices]

    return output

def infer_score(poem_text, model=Literal["gpt-5.4", "gpt-5.3", "claude-opus-4-6", "claude-sonnet-4-6", "gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview"]):
    prompt = f"Evaluate the following poem and provide a score from 1 to 10 for each of the following categories: technical craft, structure, diction, originality, and impact. Provide a detailed rationale for each score.\n\nPoem:\n{poem_text}"
    output = run_model(prompt, ScoreInference, model, temperature=0.0)

    aggregate_score = (output['technical_craft_score'] + output['structure_score'] + output['diction_score'] + output['originality_score'] + output['impact_score'])

    output["aggregate_score"] = aggregate_score

    return output
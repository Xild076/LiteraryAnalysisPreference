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


from __future__ import annotations

import json
import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

OPENAI_API_KEY = None
ANTHROPIC_API_KEY = None
GOOGLE_API_KEY = None

SUPPORTED_MODELS = (
    "gpt-5.4",
    "gpt-5.3",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite-preview",
)


def load_api_keys() -> None:
    load_dotenv()
    global OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


load_api_keys()



def _require_api_key(value: str | None, env_var: str, model: str) -> str:
    if value:
        return value
    raise RuntimeError(f"Missing {env_var} for model '{model}'")



def run_openai_models(prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 400) -> str:
    try:
        from openai import OpenAI
    except ModuleNotFoundError as exc:
        raise RuntimeError("OpenAI SDK is not installed") from exc
    client = OpenAI(api_key=_require_api_key(OPENAI_API_KEY, "OPENAI_API_KEY", model))
    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    return response.output_text



def run_anthropic_models(prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 400) -> str:
    try:
        from anthropic import Anthropic
    except ModuleNotFoundError as exc:
        raise RuntimeError("Anthropic SDK is not installed") from exc
    client = Anthropic(api_key=_require_api_key(ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY", model))
    response = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    text_parts = [block.text for block in response.content if hasattr(block, "text")]
    return "\n".join(text_parts)



def run_google_models(prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 400) -> str:
    try:
        from google import genai
    except ModuleNotFoundError as exc:
        raise RuntimeError("Google GenAI SDK is not installed") from exc
    client = genai.Client(api_key=_require_api_key(GOOGLE_API_KEY, "GOOGLE_API_KEY", model))
    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=genai.types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    return response.text



def run_model(
    prompt: str,
    schema: type[BaseModel],
    model: Literal[
        "gpt-5.4",
        "gpt-5.3",
        "claude-opus-4-6",
        "claude-sonnet-4-6",
        "gemini-3.1-pro-preview",
        "gemini-3.1-flash-lite-preview",
    ],
    temperature: float = 0.7,
    max_tokens: int = 400,
) -> dict:
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model specified: {model}")
    if model.startswith("gpt"):
        model_run_function = run_openai_models
    elif model.startswith("claude"):
        model_run_function = run_anthropic_models
    else:
        model_run_function = run_google_models
    schema_json = schema.model_json_schema()
    prompt_text = (
        f"{prompt}\n\n"
        "Return only valid JSON matching this schema exactly. Do not add markdown or code fences.\n"
        f"{json.dumps(schema_json)}"
    )
    output = model_run_function(prompt_text, model, temperature, max_tokens)
    return parse_output_json(output, schema)



def parse_output_json(output: str, schema: type[BaseModel]) -> dict:
    try:
        cleaned_output = output.replace("```json", "").replace("```", "").strip()
        return schema.model_validate_json(cleaned_output).model_dump()
    except Exception as exc:
        raise ValueError(f"Failed to parse output as JSON: {exc}") from exc

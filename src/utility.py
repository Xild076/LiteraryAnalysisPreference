from openai import OpenAI
from google import genai
from anthropic import Anthropic

from dotenv import load_dotenv
import os

from pydantic import BaseModel
from typing import Literal

OPENAI_API_KEY = None
ANTHROPIC_API_KEY = None
GOOGLE_API_KEY = None

def load_api_keys():
    load_dotenv()
    global OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

load_api_keys()


def run_openai_models(prompt, model, temperature=0.7, max_tokens=150):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.output_text

def run_anthropic_models(prompt, model, temperature=0.7, max_tokens=150):
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.content

def run_google_models(prompt, model, temperature=0.7, max_tokens=150):
    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=genai.types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
    )

    return response.text


def run_model(prompt, schema:BaseModel, model:Literal["gpt-5.4", "gpt-5.3", "claude-opus-4-6", "claude-sonnet-4-6", "gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview"], temperature=0.7, max_tokens=150):
    model_run_function = None

    if "gpt" in model:
        model_run_function = run_openai_models
    elif "claude" in model:
        model_run_function = run_anthropic_models
    elif "gemini" in model:
        model_run_function = run_google_models
    else:
        raise ValueError("Unsupported model specified")
    
    prompt_text = f"{prompt}\n\nPlease format the output as JSON matching the following schema:\n{dict(schema)}"

    output = model_run_function(prompt_text, model, temperature, max_tokens)

    return parse_output_json(output, schema)

def parse_output_json(output, schema:BaseModel):
    try:
        output = output.replace("```json", "").replace("```", "")
        return dict(schema.model_validate(output))
    except Exception as e:
        raise ValueError(f"Failed to parse output as JSON: {e}")
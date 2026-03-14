from __future__ import annotations

import json
import os
import random
import re
import time
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import BaseModel

from .logger import get_logger

logger = get_logger(__name__)

OPENAI_API_KEY = None
ANTHROPIC_API_KEY = None
GOOGLE_API_KEY = None
NVIDIA_API_KEY = None


def _read_float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value > 0 else default


def _read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value >= 0 else default


MODEL_REQUEST_TIMEOUT_SECONDS = _read_float_env("MODEL_REQUEST_TIMEOUT_SECONDS", 120.0)
MODEL_RETRY_ATTEMPTS = max(1, _read_int_env("MODEL_RETRY_ATTEMPTS", 4))
MODEL_BACKOFF_SHORT_TIER_RETRIES = max(1, _read_int_env("MODEL_BACKOFF_SHORT_TIER_RETRIES", 2))
MODEL_BACKOFF_SHORT_BASE_SECONDS = _read_float_env("MODEL_BACKOFF_SHORT_BASE_SECONDS", 0.8)
MODEL_BACKOFF_LONG_BASE_SECONDS = _read_float_env("MODEL_BACKOFF_LONG_BASE_SECONDS", 12.0)
MODEL_BACKOFF_MAX_SECONDS = _read_float_env("MODEL_BACKOFF_MAX_SECONDS", 60.0)
MODEL_BACKOFF_JITTER_SECONDS = _read_float_env("MODEL_BACKOFF_JITTER_SECONDS", 0.25)

NVIDIA_RATE_LIMIT_MAX_RETRIES = _read_int_env("NVIDIA_RATE_LIMIT_MAX_RETRIES", 5)
NVIDIA_RATE_LIMIT_SHORT_TIER_RETRIES = max(1, _read_int_env("NVIDIA_RATE_LIMIT_SHORT_TIER_RETRIES", 2))
NVIDIA_RATE_LIMIT_BASE_BACKOFF_SECONDS = _read_float_env("NVIDIA_RATE_LIMIT_BASE_BACKOFF_SECONDS", 2.0)
NVIDIA_RATE_LIMIT_LONG_BACKOFF_SECONDS = _read_float_env("NVIDIA_RATE_LIMIT_LONG_BACKOFF_SECONDS", 12.0)
NVIDIA_RATE_LIMIT_MAX_BACKOFF_SECONDS = _read_float_env("NVIDIA_RATE_LIMIT_MAX_BACKOFF_SECONDS", 60.0)
NVIDIA_RATE_LIMIT_JITTER_SECONDS = _read_float_env("NVIDIA_RATE_LIMIT_JITTER_SECONDS", 0.4)

SUPPORTED_MODELS = (
    "gpt-5.4",
    "gpt-5.3",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite-preview",
    "gemma-3-27b-it",
    "qwen/qwen3.5-397b-a17b",
    "deepseek-ai/deepseek-v3.2",
    "openai/gpt-oss-120b",
    "moonshotai/kimi-k2-instruct",
    "nemotron-3-nano-30b-a3b",
    "nemotron-3-super-120b-a12b",
)

MODEL_BACKENDS: dict[str, str] = {
    "gpt-5.4": "openai",
    "gpt-5.3": "openai",
    "claude-opus-4-6": "anthropic",
    "claude-sonnet-4-6": "anthropic",
    "gemini-3.1-pro-preview": "google",
    "gemini-3.1-flash-lite-preview": "google",
    "gemma-3-27b-it": "nvidia",
    "qwen/qwen3.5-397b-a17b": "nvidia",
    "deepseek-ai/deepseek-v3.2": "nvidia",
    "openai/gpt-oss-120b": "nvidia",
    "moonshotai/kimi-k2-instruct": "nvidia",
    "nemotron-3-nano-30b-a3b": "nvidia",
    "nemotron-3-super-120b-a12b": "nvidia",
}

NVIDIA_CANONICAL_MODEL_IDS: dict[str, str] = {
    "gemma-3-27b-it": "google/gemma-3-27b-it",
    "nemotron-3-nano-30b-a3b": "nvidia/nemotron-3-nano-30b-a3b",
    "nemotron-3-super-120b-a12b": "nvidia/nemotron-3-super-120b-a12b",
}

SupportedModel = Literal[
    "gpt-5.4",
    "gpt-5.3",
    "claude-opus-4-6",
    "claude-sonnet-4-6",
    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite-preview",
    "gemma-3-27b-it",
    "qwen/qwen3.5-397b-a17b",
    "deepseek-ai/deepseek-v3.2",
    "openai/gpt-oss-120b",
    "moonshotai/kimi-k2-instruct",
    "nemotron-3-nano-30b-a3b",
    "nemotron-3-super-120b-a12b",
]


def load_api_keys() -> None:
    load_dotenv()
    global OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, NVIDIA_API_KEY
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")


load_api_keys()



def _require_api_key(value: str | None, env_var: str, model: str) -> str:
    if value:
        return value
    raise RuntimeError(f"Missing {env_var} for model '{model}'")


def _is_retriable_json_error(exc: ValueError) -> bool:
    text = str(exc).lower()
    retriable_markers = (
        "truncated_json",
        "schema_echo_json",
        "eof while parsing",
        "unterminated",
        "unexpected end",
        "end of string",
    )
    return any(marker in text for marker in retriable_markers)


def _is_retriable_backend_error(exc: RuntimeError) -> bool:
    text = str(exc).lower()
    retriable_markers = (
        "empty content",
        "returned no choices",
        "timed out",
        "timeout",
        "connection error",
        "connect error",
        "api connection error",
        "too many requests",
        "rate limit",
        "error code: 429",
        "status': 429",
        "temporary failure",
        "length limit",
    )
    return any(marker in text for marker in retriable_markers)


def _is_timeout_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return "timed out" in text or "timeout" in text


def _is_rate_limited_error(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None)
    if status_code == 429:
        return True
    response = getattr(exc, "response", None)
    response_status_code = getattr(response, "status_code", None)
    if response_status_code == 429:
        return True
    text = str(exc).lower()
    return (
        "too many requests" in text
        or "rate limit" in text
        or "error code: 429" in text
        or "status': 429" in text
        or '"status": 429' in text
    )


def _retry_after_seconds_from_exception(exc: Exception) -> float | None:
    header_values: list[str] = []
    response = getattr(exc, "response", None)
    response_headers = getattr(response, "headers", None)
    if isinstance(response_headers, dict):
        for key in ("retry-after", "Retry-After"):
            value = response_headers.get(key)
            if value is not None:
                header_values.append(str(value))
    direct_headers = getattr(exc, "headers", None)
    if isinstance(direct_headers, dict):
        for key in ("retry-after", "Retry-After"):
            value = direct_headers.get(key)
            if value is not None:
                header_values.append(str(value))

    for value in header_values:
        try:
            seconds = float(value)
        except ValueError:
            continue
        if seconds > 0:
            return seconds

    match = re.search(r"retry[ -]?after[^0-9]*([0-9]+(?:\.[0-9]+)?)", str(exc).lower())
    if match:
        try:
            seconds = float(match.group(1))
        except ValueError:
            return None
        if seconds > 0:
            return seconds
    return None


def _two_tier_exponential_backoff_seconds(
    retry_index: int,
    *,
    short_tier_retries: int,
    short_base_seconds: float,
    long_base_seconds: float,
    max_backoff_seconds: float,
    jitter_seconds: float,
) -> float:
    capped_retry_index = max(0, int(retry_index))
    short_window = max(1, int(short_tier_retries))
    if capped_retry_index < short_window:
        base_delay = short_base_seconds * (2 ** capped_retry_index)
    else:
        long_tier_index = capped_retry_index - short_window
        base_delay = long_base_seconds * (2 ** long_tier_index)
    bounded_delay = min(base_delay, max_backoff_seconds)
    jitter = random.uniform(0.0, max(0.0, jitter_seconds))
    return bounded_delay + jitter


def _rate_limit_sleep_seconds(attempt_index: int, exc: Exception) -> float:
    retry_after_seconds = _retry_after_seconds_from_exception(exc)
    if retry_after_seconds is not None:
        base_delay = retry_after_seconds
        bounded_delay = min(base_delay, NVIDIA_RATE_LIMIT_MAX_BACKOFF_SECONDS)
        jitter = random.uniform(0.0, max(0.0, NVIDIA_RATE_LIMIT_JITTER_SECONDS))
        return bounded_delay + jitter
    return _two_tier_exponential_backoff_seconds(
        attempt_index,
        short_tier_retries=NVIDIA_RATE_LIMIT_SHORT_TIER_RETRIES,
        short_base_seconds=NVIDIA_RATE_LIMIT_BASE_BACKOFF_SECONDS,
        long_base_seconds=NVIDIA_RATE_LIMIT_LONG_BACKOFF_SECONDS,
        max_backoff_seconds=NVIDIA_RATE_LIMIT_MAX_BACKOFF_SECONDS,
        jitter_seconds=NVIDIA_RATE_LIMIT_JITTER_SECONDS,
    )


def _is_long_tier_backend_error(exc: Exception) -> bool:
    text = str(exc).lower()
    long_tier_markers = (
        "timed out",
        "timeout",
        "connection error",
        "connect error",
        "api connection error",
        "too many requests",
        "rate limit",
        "error code: 429",
        "status': 429",
        '"status": 429',
    )
    return any(marker in text for marker in long_tier_markers)


def _backend_retry_sleep_seconds(retry_index: int, exc: Exception) -> float:
    if _is_long_tier_backend_error(exc):
        return _two_tier_exponential_backoff_seconds(
            retry_index,
            short_tier_retries=MODEL_BACKOFF_SHORT_TIER_RETRIES,
            short_base_seconds=MODEL_BACKOFF_SHORT_BASE_SECONDS,
            long_base_seconds=MODEL_BACKOFF_LONG_BASE_SECONDS,
            max_backoff_seconds=MODEL_BACKOFF_MAX_SECONDS,
            jitter_seconds=MODEL_BACKOFF_JITTER_SECONDS,
        )
    # Non-timeout retriable backend failures still back off, but stay on the short tier.
    return _two_tier_exponential_backoff_seconds(
        retry_index,
        short_tier_retries=max(10, MODEL_BACKOFF_SHORT_TIER_RETRIES),
        short_base_seconds=MODEL_BACKOFF_SHORT_BASE_SECONDS,
        long_base_seconds=MODEL_BACKOFF_LONG_BASE_SECONDS,
        max_backoff_seconds=MODEL_BACKOFF_MAX_SECONDS,
        jitter_seconds=MODEL_BACKOFF_JITTER_SECONDS,
    )


def _create_nvidia_chat_completion_with_backoff(
    client: Any,
    request_kwargs: dict[str, Any],
    *,
    candidate: str,
    variant_tag: str,
) -> Any:
    max_attempts = max(1, NVIDIA_RATE_LIMIT_MAX_RETRIES + 1)
    for attempt_index in range(max_attempts):
        try:
            return client.chat.completions.create(**request_kwargs)
        except Exception as exc:
            if not _is_rate_limited_error(exc) or attempt_index >= max_attempts - 1:
                raise
            sleep_seconds = _rate_limit_sleep_seconds(attempt_index, exc)
            logger.warning(
                "NVIDIA rate-limited for candidate=%s variant=%s; pausing %.2fs before retry %d/%d",
                candidate,
                variant_tag,
                sleep_seconds,
                attempt_index + 1,
                max_attempts - 1,
            )
            time.sleep(sleep_seconds)



def _strip_code_fences(text: str) -> str:
    return text.replace("```json", "").replace("```JSON", "").replace("```", "").strip()



def _skip_json_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index



def _merge_json_objects(values: list[dict[str, Any]]) -> dict[str, Any] | None:
    merged: dict[str, Any] = {}
    for value in values:
        overlap = set(merged) & set(value)
        if overlap:
            return None
        merged.update(value)
    return merged



def _decode_json_candidates(text: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()

    for start, char in enumerate(text):
        if char != "{":
            continue
        try:
            first_value, cursor = decoder.raw_decode(text, start)
        except json.JSONDecodeError:
            continue
        if not isinstance(first_value, dict):
            continue

        values = [first_value]
        while True:
            cursor = _skip_json_whitespace(text, cursor)
            if cursor >= len(text) or text[cursor] != "{":
                break
            try:
                next_value, next_cursor = decoder.raw_decode(text, cursor)
            except json.JSONDecodeError:
                break
            if not isinstance(next_value, dict):
                break
            values.append(next_value)
            cursor = next_cursor

        merged = _merge_json_objects(values)
        if merged is None:
            merged = first_value
        candidate_key = json.dumps(merged, sort_keys=True)
        if candidate_key in seen:
            continue
        seen.add(candidate_key)
        candidates.append(merged)
    return candidates



def _looks_like_truncated_json(message: str) -> bool:
    lowered = message.lower()
    return any(
        marker in lowered
        for marker in (
            "eof while parsing",
            "unterminated",
            "unexpected end",
            "end of string",
        )
    )



def _output_preview(text: str, limit: int = 200) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return f"{compact[:limit].rstrip()}..."


def _schema_type_hint(field_schema: dict[str, Any]) -> str:
    type_value = field_schema.get("type")
    if isinstance(type_value, list):
        values = [str(item) for item in type_value if str(item).lower() != "null"]
        return "/".join(values) if values else "value"
    if isinstance(type_value, str) and type_value.strip():
        return type_value
    return "value"


def _schema_field_requirement(name: str, field_schema: dict[str, Any]) -> str:
    base_type = _schema_type_hint(field_schema)
    if base_type == "array":
        item_schema = field_schema.get("items")
        if isinstance(item_schema, dict):
            item_type = _schema_type_hint(item_schema)
            if item_type != "value":
                base_type = f"array[{item_type}]"

    details = [base_type]
    minimum = field_schema.get("minimum")
    maximum = field_schema.get("maximum")
    if minimum is not None and maximum is not None:
        details.append(f"range {minimum}..{maximum}")
    elif minimum is not None:
        details.append(f">= {minimum}")
    elif maximum is not None:
        details.append(f"<= {maximum}")

    enum_values = field_schema.get("enum")
    if isinstance(enum_values, list) and enum_values:
        enum_preview = ", ".join(json.dumps(value) for value in enum_values[:6])
        suffix = "..." if len(enum_values) > 6 else ""
        details.append(f"enum: {enum_preview}{suffix}")

    description = field_schema.get("description")
    if isinstance(description, str) and description.strip():
        details.append(description.strip())

    return f'- "{name}": {"; ".join(details)}'


def _ordered_required_fields(schema: type[BaseModel], schema_json: dict[str, Any]) -> list[str]:
    required_raw = schema_json.get("required")
    required_set = set(required_raw) if isinstance(required_raw, list) else set(schema.model_fields)
    ordered = [name for name in schema.model_fields if name in required_set]
    return ordered if ordered else list(schema.model_fields)


def _build_structured_output_prompt(
    prompt: str,
    schema: type[BaseModel],
    *,
    schema_echo_retry: bool = False,
) -> str:
    schema_json = schema.model_json_schema()
    properties = schema_json.get("properties") if isinstance(schema_json.get("properties"), dict) else {}
    required_fields = _ordered_required_fields(schema, schema_json)
    required_keys = ", ".join(json.dumps(name) for name in required_fields)

    lines = [
        "Return only one JSON object.",
        f"Include exactly these required keys: {required_keys}.",
        "Do not add extra keys, markdown, comments, or explanations.",
        "Do not output schema keywords such as properties, required, type, title, or $defs.",
        "Field requirements:",
    ]
    lines.extend(_schema_field_requirement(name, properties.get(name, {})) for name in required_fields)

    if schema_echo_retry:
        lines.insert(
            0,
            "Previous output returned JSON schema metadata. Return concrete field values instead.",
        )
    return f"{prompt}\n\n" + "\n".join(lines)


def _looks_like_schema_echo(candidate: Any, schema: type[BaseModel]) -> bool:
    if not isinstance(candidate, dict):
        return False
    expected_fields = set(schema.model_fields)
    if expected_fields and expected_fields.issubset(candidate):
        return False
    canonical_schema = schema.model_json_schema()
    if candidate == canonical_schema:
        return True
    props = candidate.get("properties")
    required = candidate.get("required")
    if not isinstance(props, dict):
        return False
    prop_names = set(props)
    required_names = set(required) if isinstance(required, list) else set()
    return bool(expected_fields) and (
        expected_fields.issubset(prop_names) or required_names == expected_fields
    )



def run_openai_models(
    prompt: str,
    model: str,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    timeout_seconds: float | None = None,
) -> str:
    try:
        from openai import OpenAI
    except ModuleNotFoundError as exc:
        raise RuntimeError("OpenAI SDK is not installed") from exc
        
    effective_timeout = MODEL_REQUEST_TIMEOUT_SECONDS if timeout_seconds is None else float(timeout_seconds)
    client = OpenAI(
        api_key=_require_api_key(OPENAI_API_KEY, "OPENAI_API_KEY", model),
        timeout=effective_timeout,
    )
    request_kwargs: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    if max_tokens is not None:
        request_kwargs["max_tokens"] = max_tokens
    response = client.chat.completions.create(**request_kwargs)
    return response.choices[0].message.content or ""



def run_anthropic_models(
    prompt: str,
    model: str,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    timeout_seconds: float | None = None,
) -> str:
    try:
        from anthropic import Anthropic
    except ModuleNotFoundError as exc:
        raise RuntimeError("Anthropic SDK is not installed") from exc
    client = Anthropic(
        api_key=_require_api_key(ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY", model),
        timeout=MODEL_REQUEST_TIMEOUT_SECONDS if timeout_seconds is None else float(timeout_seconds),
    )
    response = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens if max_tokens is not None else 4096,
    )
    text_parts = [block.text for block in response.content if hasattr(block, "text")]
    return "\n".join(text_parts)



def run_google_models(
    prompt: str,
    model: str,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    timeout_seconds: float | None = None,
) -> str:
    try:
        from google import genai
    except ModuleNotFoundError as exc:
        raise RuntimeError("Google GenAI SDK is not installed") from exc
        
    effective_timeout = MODEL_REQUEST_TIMEOUT_SECONDS if timeout_seconds is None else float(timeout_seconds)
    client = genai.Client(
        api_key=_require_api_key(GOOGLE_API_KEY, "GOOGLE_API_KEY", model),
        http_options={"timeout": effective_timeout}
    )
    config_kwargs: dict[str, Any] = {"temperature": temperature}
    if max_tokens is not None:
        config_kwargs["max_output_tokens"] = max_tokens
    response = client.models.generate_content(
        model=f"models/{model}",
        contents=[prompt],
        config=genai.types.GenerateContentConfig(**config_kwargs),
    )
    return response.text


def _nvidia_model_candidates(model: str) -> list[str]:
    base = str(model).strip()
    if "/" in base:
        return [base]
    canonical = NVIDIA_CANONICAL_MODEL_IDS.get(base)
    if canonical:
        fallbacks: list[str] = []
        if base.startswith("gemma"):
            fallbacks = [base, f"nvidia/{base}"]
        elif base.startswith("nemotron"):
            fallbacks = [base]
        return list(dict.fromkeys([canonical, *fallbacks]))
    candidates = [f"nvidia/{base}", base]
    return list(dict.fromkeys(candidates))


def _nvidia_variant_tag(variant: dict[str, Any]) -> str:
    extra_body = variant.get("extra_body")
    if not isinstance(extra_body, dict):
        return "default"
    kwargs = extra_body.get("chat_template_kwargs")
    if kwargs is None:
        return "custom"
    if not isinstance(kwargs, dict):
        return "custom"
    if "enable_thinking" in kwargs:
        return f"enable_thinking={kwargs.get('enable_thinking')}"
    if "thinking" in kwargs:
        return f"thinking={kwargs.get('thinking')}"
    if not kwargs:
        return "default"
    return "custom"


def _build_nvidia_request_kwargs(
    prompt: str,
    candidate: str,
    temperature: float,
    max_tokens: int | None,
    timeout_seconds: float,
    variant: dict[str, Any],
) -> dict[str, Any]:
    request_kwargs: dict[str, Any] = {
        "model": candidate,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "timeout": timeout_seconds,
    }
    if max_tokens is not None:
        request_kwargs["max_tokens"] = max_tokens
    for key, value in variant.items():
        if key == "extra_body" and isinstance(value, dict):
            request_kwargs["extra_body"] = dict(value)
            continue
        request_kwargs[key] = value
    return request_kwargs


def _extract_text_from_nvidia_content(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()

    def _from_part(part: Any) -> str:
        if isinstance(part, str):
            return part
        if isinstance(part, dict):
            for key in ("text", "output_text", "content", "value"):
                value = part.get(key)
                if isinstance(value, str):
                    return value
        for attr in ("text", "output_text", "content", "value"):
            value = getattr(part, attr, None)
            if isinstance(value, str):
                return value
        return ""

    if isinstance(content, list):
        pieces = [_from_part(item).strip() for item in content]
        return "\n".join(piece for piece in pieces if piece).strip()

    return ""


def _run_nvidia_candidate_variants(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    variants: list[dict[str, Any]],
    not_found_error_type: type[Exception],
) -> str:
    _ = allow_token_retry
    attempted_models = _nvidia_model_candidates(model)
    last_error: Exception | None = None

    for candidate in attempted_models:
        candidate_not_found = False
        for variant in variants:
            variant_tag = _nvidia_variant_tag(variant)
            logger.debug(
                "NVIDIA call: candidate=%s variant=%s tokens=%s",
                candidate,
                variant_tag,
                max_tokens,
            )
            request_kwargs = _build_nvidia_request_kwargs(
                prompt,
                candidate,
                temperature,
                max_tokens,
                timeout_seconds,
                variant,
            )
            try:
                response = _create_nvidia_chat_completion_with_backoff(
                    client,
                    request_kwargs,
                    candidate=candidate,
                    variant_tag=variant_tag,
                )
            except not_found_error_type as exc:
                logger.debug("NVIDIA 404 for candidate=%s: %s", candidate, exc)
                last_error = exc
                candidate_not_found = True
                break
            except Exception as exc:
                logger.debug("NVIDIA error for candidate=%s: %s", candidate, exc)
                last_error = exc
                if _is_timeout_error(exc):
                    logger.warning(
                        "NVIDIA timeout for candidate=%s variant=%s; trying next variant",
                        candidate,
                        variant_tag,
                    )
                continue

            if not response.choices:
                last_error = RuntimeError(f"NVIDIA returned no choices for model '{candidate}'")
                continue

            choice = response.choices[0]
            text = _extract_text_from_nvidia_content(choice.message.content)
            if text:
                return text

            finish_reason = getattr(choice, "finish_reason", None)
            if finish_reason == "length":
                last_error = RuntimeError(f"NVIDIA response hit length limit for model '{candidate}'")
                continue
            last_error = RuntimeError(f"NVIDIA returned empty content for model '{candidate}'")

        if candidate_not_found:
            continue

    reason = str(last_error) if last_error is not None else "unknown_error"
    raise RuntimeError(
        f"NVIDIA request failed for '{model}'. Tried: {', '.join(attempted_models)}. Last error: {reason}"
    ) from last_error


def _run_nvidia_qwen_model(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    not_found_error_type: type[Exception],
) -> str:
    variants = [
        {
            "top_p": 0.95,
            "presence_penalty": 0.0,
            "extra_body": {
                "top_k": 20,
                "repetition_penalty": 1.0,
                "chat_template_kwargs": {"enable_thinking": False},
            },
        },
        {
            "top_p": 0.95,
            "presence_penalty": 0.0,
            "extra_body": {
                "top_k": 20,
                "repetition_penalty": 1.0,
            },
        },
        {},
    ]
    return _run_nvidia_candidate_variants(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        timeout_seconds,
        variants,
        not_found_error_type,
    )


def _run_nvidia_deepseek_model(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    not_found_error_type: type[Exception],
) -> str:
    variants = [
        {"top_p": 0.95, "extra_body": {"chat_template_kwargs": {"thinking": False}}},
        {"top_p": 0.95},
        {},
    ]
    return _run_nvidia_candidate_variants(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        timeout_seconds,
        variants,
        not_found_error_type,
    )


def _run_nvidia_gpt_oss_model(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    not_found_error_type: type[Exception],
) -> str:
    variants = [
        {"top_p": 1.0, "extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        {"top_p": 1.0},
    ]
    return _run_nvidia_candidate_variants(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        timeout_seconds,
        variants,
        not_found_error_type,
    )


def _run_nvidia_kimi_model(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    not_found_error_type: type[Exception],
) -> str:
    variants = [{"top_p": 0.9}, {}]
    return _run_nvidia_candidate_variants(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        timeout_seconds,
        variants,
        not_found_error_type,
    )


def _run_nvidia_nemotron_model(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    not_found_error_type: type[Exception],
) -> str:
    variants = [
        {"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        {},
    ]
    return _run_nvidia_candidate_variants(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        timeout_seconds,
        variants,
        not_found_error_type,
    )


def _run_nvidia_gemma_model(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    not_found_error_type: type[Exception],
) -> str:
    return _run_nvidia_candidate_variants(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        timeout_seconds,
        [{}],
        not_found_error_type,
    )


def _run_nvidia_default_model(
    client: Any,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int | None,
    allow_token_retry: bool,
    timeout_seconds: float,
    not_found_error_type: type[Exception],
) -> str:
    return _run_nvidia_candidate_variants(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        timeout_seconds,
        [{}],
        not_found_error_type,
    )


def run_nvidia_models(
    prompt: str,
    model: str,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    allow_token_retry: bool = True,
    timeout_seconds: float | None = None,
) -> str:
    try:
        from openai import NotFoundError, OpenAI
    except ModuleNotFoundError as exc:
        raise RuntimeError("OpenAI SDK is not installed") from exc

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=_require_api_key(NVIDIA_API_KEY, "NVIDIA_API_KEY", model),
        max_retries=0,
    )
    effective_timeout = MODEL_REQUEST_TIMEOUT_SECONDS if timeout_seconds is None else float(timeout_seconds)

    model_lower = model.lower()
    if "qwen" in model_lower:
        return _run_nvidia_qwen_model(
            client,
            prompt,
            model,
            temperature,
            max_tokens,
            allow_token_retry,
            effective_timeout,
            NotFoundError,
        )
    if "deepseek" in model_lower:
        return _run_nvidia_deepseek_model(
            client,
            prompt,
            model,
            temperature,
            max_tokens,
            allow_token_retry,
            effective_timeout,
            NotFoundError,
        )
    if "gpt-oss" in model_lower:
        return _run_nvidia_gpt_oss_model(
            client,
            prompt,
            model,
            temperature,
            max_tokens,
            allow_token_retry,
            effective_timeout,
            NotFoundError,
        )
    if "kimi" in model_lower:
        return _run_nvidia_kimi_model(
            client,
            prompt,
            model,
            temperature,
            max_tokens,
            allow_token_retry,
            effective_timeout,
            NotFoundError,
        )
    if "nemotron" in model_lower:
        return _run_nvidia_nemotron_model(
            client,
            prompt,
            model,
            temperature,
            max_tokens,
            allow_token_retry,
            effective_timeout,
            NotFoundError,
        )
    if "gemma" in model_lower:
        return _run_nvidia_gemma_model(
            client,
            prompt,
            model,
            temperature,
            max_tokens,
            allow_token_retry,
            effective_timeout,
            NotFoundError,
        )
    return _run_nvidia_default_model(
        client,
        prompt,
        model,
        temperature,
        max_tokens,
        allow_token_retry,
        effective_timeout,
        NotFoundError,
    )


def run_model(
    prompt: str,
    schema: type[BaseModel],
    model: SupportedModel,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    disable_retries: bool = False,
    timeout_seconds: float | None = None,
) -> dict:
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model specified: {model}")

    backend = MODEL_BACKENDS.get(model)
    if backend == "openai":
        model_run_function = run_openai_models
    elif backend == "anthropic":
        model_run_function = run_anthropic_models
    elif backend == "nvidia":
        model_run_function = lambda prompt_text, model_name, temp, token_budget, timeout: run_nvidia_models(
            prompt_text,
            model_name,
            temp,
            token_budget,
            allow_token_retry=False,
            timeout_seconds=timeout,
        )
    elif backend == "google":
        model_run_function = run_google_models
    else:
        raise ValueError(f"No backend configured for model: {model}")

    schema_echo_retry_mode = False
    parse_error: ValueError | None = None
    backend_error: RuntimeError | None = None
    attempt_count = 1 if disable_retries else MODEL_RETRY_ATTEMPTS

    for attempt_index in range(attempt_count):
        prompt_text = _build_structured_output_prompt(
            prompt,
            schema,
            schema_echo_retry=schema_echo_retry_mode,
        )
        logger.debug(
            "run_model: %s backend=%s schema=%s tokens=%s attempt=%s/%s",
            model,
            backend,
            schema.__name__,
            max_tokens,
            attempt_index + 1,
            attempt_count,
        )
        try:
            output = model_run_function(prompt_text, model, temperature, max_tokens, timeout_seconds)
        except RuntimeError as exc:
            backend_error = exc
            if attempt_index == attempt_count - 1 or not _is_retriable_backend_error(exc):
                raise
            retry_index = attempt_index
            sleep_seconds = _backend_retry_sleep_seconds(retry_index, exc)
            logger.info(
                "run_model: backend error on %s (tokens=%s): %s. Retrying in %.2fs (attempt %d/%d).",
                model,
                max_tokens,
                exc,
                sleep_seconds,
                attempt_index + 2,
                attempt_count,
            )
            time.sleep(sleep_seconds)
            continue

        try:
            return parse_output_json(output, schema)
        except ValueError as exc:
            parse_error = exc
            if "schema_echo_json" in str(exc).lower():
                schema_echo_retry_mode = True
            if attempt_index == attempt_count - 1 or not _is_retriable_json_error(exc):
                raise
            sleep_seconds = min(1.5, 0.3 * (attempt_index + 1)) + random.uniform(0.0, 0.2)
            reason = "schema-echo retry" if schema_echo_retry_mode else "parse retry"
            logger.info(
                "run_model: %s on %s (tokens=%s), retrying in %.2fs (attempt %d/%d)",
                reason,
                model,
                max_tokens,
                sleep_seconds,
                attempt_index + 2,
                attempt_count,
            )
            time.sleep(sleep_seconds)

    if parse_error is not None:
        raise parse_error
    if backend_error is not None:
        raise backend_error
    raise RuntimeError("run_model failed without a parse error")



def parse_output_json(output: str, schema: type[BaseModel]) -> dict:
    cleaned_output = _strip_code_fences(output)
    if not cleaned_output:
        raise ValueError(f"Failed to parse output as JSON for {schema.__name__}: empty response")
    schema_echo_detected = False
    try:
        parsed = json.loads(cleaned_output)
    except Exception:
        parsed = None
    if _looks_like_schema_echo(parsed, schema):
        schema_echo_detected = True
    try:
        return schema.model_validate_json(cleaned_output).model_dump()
    except Exception as exc:
        for candidate in _decode_json_candidates(cleaned_output):
            if _looks_like_schema_echo(candidate, schema):
                schema_echo_detected = True
                continue
            try:
                return schema.model_validate(candidate).model_dump()
            except Exception:
                continue
        if schema_echo_detected:
            error_kind = "schema_echo_json"
        else:
            error_kind = "truncated_json" if _looks_like_truncated_json(str(exc)) else "json_parse_error"
        raise ValueError(
            f"{error_kind}: Failed to parse output as JSON for {schema.__name__}: {exc}. "
            f"Output preview: {_output_preview(cleaned_output)!r}"
        ) from exc

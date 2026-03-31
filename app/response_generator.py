"""FLAN-T5-first empathetic response synthesis with safe fallback."""

from __future__ import annotations

import hashlib
import re
from typing import Any


_PRIMARY_RESPONSE_MODEL = "google/flan-t5-base"
_SECONDARY_RESPONSE_MODEL = "google/flan-t5-small"
_RESPONSE_MAX_NEW_TOKENS = 48

_RESPONSE_GENERATOR: Any | None = None
_RESPONSE_RUNTIME_INITIALIZED = False


def _make_response_runtime_status(
    *,
    runtime_mode: str,
    model_name: str | None,
    fallback_used: bool,
    response_runtime_active: bool,
    message: str,
    load_error: str | None = None,
    inference_error: str | None = None,
) -> dict[str, Any]:
    """Build a compact runtime-status dictionary for UI consumption."""

    status: dict[str, Any] = {
        "runtime_mode": runtime_mode,
        "model_name": model_name,
        "fallback_used": bool(fallback_used),
        "response_runtime_active": bool(response_runtime_active),
        "message": message,
    }
    if load_error:
        status["load_error"] = load_error
    if inference_error:
        status["inference_error"] = inference_error
    return status


_RESPONSE_RUNTIME_STATUS = _make_response_runtime_status(
    runtime_mode="fallback_template",
    model_name=None,
    fallback_used=True,
    response_runtime_active=False,
    message=(
        "Response runtime has not been initialized yet. "
        "FLAN-T5 will be attempted on first use."
    ),
)


def _short_error_message(exc: BaseException, limit: int = 220) -> str:
    """Return a short, readable error message for runtime status records."""

    message = f"{exc.__class__.__name__}: {exc}"
    if len(message) <= limit:
        return message
    return f"{message[: limit - 3].rstrip()}..."


def _store_response_runtime_status(status: dict[str, Any]) -> dict[str, Any]:
    """Persist the runtime status and return a defensive copy."""

    global _RESPONSE_RUNTIME_STATUS
    _RESPONSE_RUNTIME_STATUS = dict(status)
    return dict(_RESPONSE_RUNTIME_STATUS)


def _merge_response_runtime_status(**updates: Any) -> dict[str, Any]:
    """Update the runtime status while preserving unchanged fields."""

    status = dict(_RESPONSE_RUNTIME_STATUS)
    for key, value in updates.items():
        if value is None:
            status.pop(key, None)
        else:
            status[key] = value
    return _store_response_runtime_status(status)


def get_response_runtime_status() -> dict[str, Any]:
    """Return the current response runtime status."""

    return dict(_RESPONSE_RUNTIME_STATUS)


def build_response_prompt(user_text: str, fused_emotion: str) -> str:
    """Build a short prompt for FLAN-T5 empathetic response synthesis."""

    user_text = (user_text or "").strip()
    emotion = (fused_emotion or "neutral").strip().lower() or "neutral"
    return (
        "You are an empathetic assistant for an HCI research demo.\n"
        f"User utterance: {user_text}\n"
        f"Detected fused emotion: {emotion}\n\n"
        "Write 1 or 2 short sentences that are warm, supportive, "
        "context-aware, non-judgmental, and socially aware. "
        "Do not mention model labels, do not give a lecture, and keep the tone natural."
    )


def _stable_index(seed: str, size: int) -> int:
    """Return a deterministic index for the fallback template bank."""

    if size <= 0:
        return 0
    digest = hashlib.sha256(seed.encode("utf-8", errors="ignore")).hexdigest()
    return int(digest, 16) % size


_FALLBACK_RESPONSE_BANK = {
    "happy": [
        "That sounds encouraging. I'm glad there's something positive to build on.",
        "Nice, that feels like good momentum. I'm happy to help keep it moving.",
        "That comes across as a good sign. We can build on it calmly.",
        "That's a positive note, and it's worth acknowledging.",
    ],
    "sad": [
        "I'm sorry this feels heavy. We can take it one small step at a time.",
        "That sounds difficult. If you want, we can focus on the next manageable step.",
        "I hear that this is weighing on you. I'll stay calm and keep this practical.",
        "That sounds painful. We can slow down and work through it gently.",
    ],
    "angry": [
        "That sounds frustrating. We can keep this practical and focus on what matters most.",
        "I can hear the tension there. Let's slow it down and make the next step clear.",
        "That feels understandably frustrating. I'll keep the response grounded and helpful.",
        "That sounds heated. We can break it into something more manageable.",
    ],
    "neutral": [
        "Thanks for sharing. I'll keep this focused and helpful.",
        "Understood. We can stay practical and move forward from here.",
        "That sounds steady. I'm ready to help with the next step.",
        "I appreciate the update. Let's keep it clear and useful.",
    ],
    "fear": [
        "That sounds uncertain. We can break it into one clear next step.",
        "I hear the worry there. Let's make it feel more manageable.",
        "That seems tense. We can slow down and clarify what matters most.",
        "This sounds a bit overwhelming, so I'll help keep it simple.",
    ],
    "surprise": [
        "That feels unexpected. We can sort through it calmly.",
        "Interesting, that sounds sudden. I can help make sense of it.",
        "That's a surprise. Let's look at it piece by piece.",
        "That seems unexpected, and we can take a measured look at it.",
    ],
    "disgust": [
        "That sounds unpleasant. We can steer toward something more comfortable.",
        "I hear that this feels off. Let's move toward a better path.",
        "That sounds strongly negative. I'll keep this calm and practical.",
        "That's a tough reaction. We can focus on what would feel more workable.",
    ],
}


def generate_response_fallback(user_text: str, fused_emotion: str) -> str:
    """Generate a polished template fallback response."""

    emotion = (fused_emotion or "neutral").strip().lower() or "neutral"
    options = _FALLBACK_RESPONSE_BANK.get(emotion, _FALLBACK_RESPONSE_BANK["neutral"])
    seed = f"{emotion}|{(user_text or '').strip()}"
    return options[_stable_index(seed, len(options))]


def _extract_generated_text(result: Any) -> str:
    """Extract generated text from a text2text-generation pipeline response."""

    payload = result
    if isinstance(payload, list):
        payload = payload[0] if payload else {}

    if isinstance(payload, str):
        return payload

    if isinstance(payload, dict):
        for key in ("generated_text", "text", "summary_text"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
    return ""


def _clean_generated_response(text: str, *, max_sentences: int = 2, max_chars: int = 220) -> str:
    """Normalize generated text into a concise classroom-demo response."""

    cleaned = re.sub(r"\s+", " ", (text or "")).strip()
    if not cleaned:
        return ""

    for prefix in ("Response:", "Assistant:", "Reply:", "Answer:"):
        if cleaned.lower().startswith(prefix.lower()):
            cleaned = cleaned[len(prefix) :].strip()
            break

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    if len(sentences) > max_sentences:
        cleaned = " ".join(sentences[:max_sentences]).strip()

    if len(cleaned) > max_chars:
        trimmed = cleaned[:max_chars].rsplit(" ", 1)[0].strip(" ,;:-")
        cleaned = trimmed if trimmed else cleaned[:max_chars].strip()

    if cleaned and cleaned[-1] not in ".!?":
        cleaned += "."

    return cleaned


def _load_text2text_pipeline(model_name: str) -> Any:
    """Load a Hugging Face text2text generation pipeline."""

    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=model_name,
        tokenizer=model_name,
    )


def _attempt_response_runtime_initialization() -> tuple[Any | None, dict[str, Any]]:
    """Attempt to initialize the FLAN-T5 runtime."""

    load_errors: list[str] = []
    for model_name in (_PRIMARY_RESPONSE_MODEL, _SECONDARY_RESPONSE_MODEL):
        try:
            generator = _load_text2text_pipeline(model_name)
            if model_name == _PRIMARY_RESPONSE_MODEL:
                message = (
                    "FLAN-T5 response runtime loaded successfully and is ready "
                    "for empathetic generation."
                )
            else:
                message = (
                    f"{_PRIMARY_RESPONSE_MODEL} was unavailable, so "
                    f"{_SECONDARY_RESPONSE_MODEL} was loaded successfully."
                )
            status = _make_response_runtime_status(
                runtime_mode="flan_t5",
                model_name=model_name,
                fallback_used=False,
                response_runtime_active=True,
                message=message,
            )
            return generator, status
        except Exception as exc:
            load_errors.append(f"{model_name}: {_short_error_message(exc)}")

    load_error = "; ".join(load_errors) if load_errors else "FLAN-T5 could not be loaded."
    status = _make_response_runtime_status(
        runtime_mode="fallback_template",
        model_name=None,
        fallback_used=True,
        response_runtime_active=False,
        message=(
            "FLAN-T5 could not be loaded. Using the safe template fallback "
            "response generator."
        ),
        load_error=_short_error_message(RuntimeError(load_error)),
    )
    return None, status


def initialize_response_runtime() -> dict[str, Any]:
    """Explicitly initialize and cache the response-generation runtime."""

    global _RESPONSE_GENERATOR, _RESPONSE_RUNTIME_INITIALIZED

    if _RESPONSE_RUNTIME_INITIALIZED:
        return get_response_runtime_status()

    generator, status = _attempt_response_runtime_initialization()
    _RESPONSE_GENERATOR = generator
    _RESPONSE_RUNTIME_INITIALIZED = True
    return _store_response_runtime_status(status)


def _generate_with_runtime(prompt: str) -> str:
    """Generate a response using the active FLAN-T5 runtime."""

    if _RESPONSE_GENERATOR is None:
        raise RuntimeError("Response runtime is not initialized.")

    output = _RESPONSE_GENERATOR(
        prompt,
        max_new_tokens=_RESPONSE_MAX_NEW_TOKENS,
        do_sample=False,
        num_beams=2,
        temperature=0.0,
        truncation=True,
    )
    generated_text = _extract_generated_text(output)
    return _clean_generated_response(generated_text)


def generate_response(user_text: str, fused_emotion: str) -> str:
    """Generate a concise empathetic response with FLAN-T5 first."""

    initialize_response_runtime()

    runtime_status = get_response_runtime_status()
    if runtime_status.get("response_runtime_active", False) and _RESPONSE_GENERATOR is not None:
        try:
            prompt = build_response_prompt(user_text, fused_emotion)
            response = _generate_with_runtime(prompt)
            if not response:
                raise RuntimeError("FLAN-T5 returned an empty response.")
            _merge_response_runtime_status(
                fallback_used=False,
                message="FLAN-T5 generated the response for this turn.",
                inference_error=None,
            )
            return response
        except Exception as exc:
            error_message = _short_error_message(exc)
            _merge_response_runtime_status(
                fallback_used=True,
                message=(
                    "FLAN-T5 generation failed for this turn. "
                    "Using the safe template fallback response generator."
                ),
                inference_error=error_message,
            )
            return generate_response_fallback(user_text, fused_emotion)

    return generate_response_fallback(user_text, fused_emotion)

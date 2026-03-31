"""Transformer-first text emotion runtime with emergency-only fallback."""

from __future__ import annotations

import re
from typing import Any

try:
    from app.utils import normalize_probs
except ImportError:  # pragma: no cover - supports running from app/ directly
    from utils import normalize_probs

EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]

_TEXT_MODEL_NAME = "SamLowe/roberta-base-go_emotions"

_TEXT_PIPELINE: Any | None = None


def _make_runtime_status(
    *,
    runtime_mode: str,
    fallback_used: bool,
    transformer_active: bool,
    message: str,
    model_name: str | None = None,
    load_error: str | None = None,
) -> dict[str, Any]:
    """Build a compact runtime-status dictionary for UI consumption."""

    status: dict[str, Any] = {
        "runtime_mode": runtime_mode,
        "model_name": model_name if model_name is not None else _TEXT_MODEL_NAME,
        "fallback_used": bool(fallback_used),
        "transformer_active": bool(transformer_active),
        "message": message,
    }
    if load_error:
        status["load_error"] = load_error
    return status


_TEXT_RUNTIME_STATUS = _make_runtime_status(
    runtime_mode="fallback_rule_based",
    fallback_used=True,
    transformer_active=False,
    message=(
        "Transformer runtime has not been initialized yet. "
        "The emergency rule-based fallback is ready if needed."
    ),
)


def _short_error_message(exc: BaseException, limit: int = 220) -> str:
    """Return a short, readable error message for runtime status records."""

    message = f"{exc.__class__.__name__}: {exc}"
    if len(message) <= limit:
        return message
    return f"{message[: limit - 3].rstrip()}..."


_MODEL_LABEL_TO_PROJECT = {
    "anger": "angry",
    "annoyance": "angry",
    "approval": "happy",
    "caring": "happy",
    "desire": "happy",
    "disapproval": "angry",
    "disappointment": "sad",
    "disgust": "disgust",
    "embarrassment": "sad",
    "excitement": "happy",
    "fear": "fear",
    "gratitude": "happy",
    "grief": "sad",
    "happiness": "happy",
    "hope": "happy",
    "joy": "happy",
    "joyful": "happy",
    "love": "happy",
    "nervousness": "fear",
    "optimism": "happy",
    "pride": "happy",
    "realization": "surprise",
    "relief": "happy",
    "remorse": "sad",
    "sad": "sad",
    "sadness": "sad",
    "surprise": "surprise",
    "astonishment": "surprise",
    "amusement": "happy",
    "admiration": "happy",
    "anxiety": "fear",
    "confusion": "neutral",
    "curiosity": "neutral",
    "frustration": "angry",
    "neutral": "neutral",
    "positive": "happy",
    "negative": "sad",
}

_KEYWORD_BANKS = {
    "happy": {
        "happy": 2.2,
        "excited": 2.0,
        "great": 1.8,
        "awesome": 2.0,
        "good": 1.0,
        "glad": 1.5,
        "pleased": 1.4,
        "proud": 1.3,
        "relieved": 1.4,
        "joy": 1.8,
        "wonderful": 2.1,
        "love it": 1.7,
        "grateful": 1.8,
        "thankful": 1.7,
        "content": 1.3,
        "delighted": 2.0,
        "hopeful": 1.4,
        "smiling": 1.2,
        "feeling good": 1.6,
    },
    "sad": {
        "sad": 2.2,
        "upset": 1.8,
        "down": 1.3,
        "tired": 1.1,
        "lonely": 1.7,
        "hurt": 1.5,
        "blue": 1.2,
        "disappointed": 1.8,
        "discouraged": 1.5,
        "miserable": 2.0,
        "heartbroken": 2.2,
        "depressed": 2.2,
        "crying": 1.8,
        "rough day": 1.4,
        "not okay": 2.0,
        "not good": 1.8,
        "feeling low": 1.6,
        "bad day": 1.5,
    },
    "angry": {
        "angry": 2.3,
        "mad": 2.0,
        "frustrated": 2.1,
        "annoyed": 1.7,
        "furious": 2.3,
        "irritated": 1.8,
        "fed up": 1.9,
        "bothered": 1.2,
        "rage": 2.2,
        "resentful": 1.5,
        "stressed": 1.1,
        "pissed": 2.1,
        "hate": 1.9,
        "unfair": 1.6,
        "can't stand": 1.8,
    },
    "neutral": {
        "okay": 1.8,
        "ok": 1.8,
        "fine": 1.7,
        "alright": 1.5,
        "steady": 1.1,
        "calm": 1.0,
        "normal": 1.0,
        "manageable": 1.0,
        "mixed": 0.9,
        "so so": 1.3,
        "just checking": 1.0,
        "for now": 0.8,
        "usual": 0.8,
        "average": 0.7,
    },
    "fear": {
        "worried": 2.1,
        "anxious": 2.2,
        "scared": 2.1,
        "nervous": 1.9,
        "afraid": 2.2,
        "uncertain": 1.7,
        "uneasy": 1.6,
        "tense": 1.3,
        "overwhelmed": 1.8,
        "not sure": 1.7,
        "concerned": 1.5,
        "panic": 2.2,
        "unsafe": 2.0,
        "threatened": 1.8,
    },
    "surprise": {
        "surprised": 2.1,
        "shocked": 2.2,
        "wow": 1.4,
        "unexpected": 1.9,
        "amazed": 1.8,
        "astonished": 2.0,
        "suddenly": 1.0,
        "didn't expect": 1.8,
        "unbelievable": 1.9,
        "taken aback": 1.7,
        "what a surprise": 2.0,
    },
    "disgust": {
        "disgusted": 2.3,
        "gross": 1.9,
        "nasty": 1.8,
        "ew": 1.5,
        "repulsed": 2.1,
        "revolting": 2.1,
        "sickening": 2.0,
        "icky": 1.6,
        "unpleasant": 1.3,
        "grossed out": 2.0,
        "repulsive": 2.1,
    },
}

_NEUTRAL_HINTS = {
    "fine",
    "okay",
    "ok",
    "alright",
    "mixed",
    "so so",
    "just checking",
    "for now",
    "usual",
    "average",
}


def _set_runtime_status(status: dict[str, Any]) -> None:
    """Persist the latest text-runtime status for the Streamlit UI."""

    global _TEXT_RUNTIME_STATUS
    _TEXT_RUNTIME_STATUS = dict(status)


def get_text_runtime_status() -> dict[str, Any]:
    """Return the most recent text-emotion runtime status."""

    return dict(_TEXT_RUNTIME_STATUS)


def get_text_emotion_backend_status() -> dict[str, Any]:
    """Compatibility alias for older imports in the app."""

    return get_text_runtime_status()


def normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    """Normalize raw emotion scores into the project schema."""

    aligned = {emotion: float(scores.get(emotion, 0.0)) for emotion in EMOTIONS}
    return normalize_probs(aligned)


def _count_term(term: str, text_lower: str) -> int:
    """Count exact term matches in the normalized text string."""

    pattern = rf"\b{re.escape(term)}\b"
    return len(re.findall(pattern, text_lower))


def _clean_text(text: str | None) -> str:
    """Normalize free text to a lowercase word stream for rule-based scoring."""

    return " ".join(re.findall(r"[a-z']+", (text or "").lower()))


def _normalize_model_label(label: Any) -> str:
    """Normalize pipeline labels before projecting them into the 7-class schema."""

    normalized = str(label or "").strip().lower()
    normalized = normalized.replace("-", "_").replace(" ", "_")
    return normalized


def _project_emotion_for_label(label: str) -> str | None:
    """Map a transformer label onto one of the seven project emotions."""

    normalized = _normalize_model_label(label)
    if not normalized:
        return None
    if normalized in EMOTIONS:
        return normalized
    return _MODEL_LABEL_TO_PROJECT.get(normalized)


def _flatten_pipeline_output(raw_output: Any) -> list[dict[str, Any]]:
    """Flatten common Hugging Face pipeline output shapes into label-score rows."""

    if raw_output is None:
        return []

    if isinstance(raw_output, dict):
        if "label" in raw_output and "score" in raw_output:
            return [raw_output]
        if (
            "labels" in raw_output
            and "scores" in raw_output
            and isinstance(raw_output["labels"], (list, tuple))
            and isinstance(raw_output["scores"], (list, tuple))
        ):
            return [
                {"label": label, "score": score}
                for label, score in zip(raw_output["labels"], raw_output["scores"])
            ]
        if "emotion" in raw_output and isinstance(raw_output["emotion"], dict):
            return [
                {"label": label, "score": score}
                for label, score in raw_output["emotion"].items()
            ]
        return [
            {"label": label, "score": score}
            for label, score in raw_output.items()
            if isinstance(score, (int, float))
        ]

    if isinstance(raw_output, (list, tuple)):
        flattened: list[dict[str, Any]] = []
        for item in raw_output:
            flattened.extend(_flatten_pipeline_output(item))
        return flattened

    return []


def _attempt_text_runtime_initialization() -> tuple[Any | None, dict[str, Any]]:
    """Load the Hugging Face text pipeline and build the matching status."""

    try:
        from transformers import pipeline
    except Exception as exc:
        metadata = _make_runtime_status(
            runtime_mode="fallback_rule_based",
            fallback_used=True,
            transformer_active=False,
            message=(
                "Transformers is unavailable. "
                "Using the emergency rule-based fallback."
            ),
            model_name=_TEXT_MODEL_NAME,
            load_error=_short_error_message(exc),
        )
        _set_runtime_status(metadata)
        return None, metadata

    try:
        classifier = pipeline(
            "text-classification",
            model=_TEXT_MODEL_NAME,
            tokenizer=_TEXT_MODEL_NAME,
            top_k=None,
            device=-1,
        )
    except Exception as exc:
        metadata = _make_runtime_status(
            runtime_mode="fallback_rule_based",
            fallback_used=True,
            transformer_active=False,
            message=(
                "Transformer text model could not be loaded. "
                "Using the emergency rule-based fallback."
            ),
            model_name=_TEXT_MODEL_NAME,
            load_error=_short_error_message(exc),
        )
        _set_runtime_status(metadata)
        return None, metadata

    metadata = _make_runtime_status(
        runtime_mode="transformer",
        fallback_used=False,
        transformer_active=True,
        message=(
            "Transformer runtime is active. "
            f"Loaded {_TEXT_MODEL_NAME} for text emotion inference."
        ),
        model_name=_TEXT_MODEL_NAME,
    )
    _set_runtime_status(metadata)
    return classifier, metadata


def initialize_text_runtime() -> dict[str, Any]:
    """Explicitly initialize and cache the transformer-based text runtime."""

    global _TEXT_PIPELINE

    if _TEXT_PIPELINE is not None and _TEXT_RUNTIME_STATUS.get("transformer_active"):
        return dict(_TEXT_RUNTIME_STATUS)

    classifier, metadata = _attempt_text_runtime_initialization()
    _TEXT_PIPELINE = classifier
    _set_runtime_status(metadata)
    return dict(metadata)


def load_text_emotion_pipeline() -> tuple[Any | None, dict[str, Any]]:
    """Load and cache the Hugging Face text-classification pipeline.

    Returns the cached pipeline object and the current runtime metadata. The
    first call explicitly attempts transformer initialization so that the
    runtime can report success or failure immediately.
    """

    initialize_text_runtime()
    return _TEXT_PIPELINE, dict(_TEXT_RUNTIME_STATUS)


def _coerce_loaded_runtime(load_result: Any) -> tuple[Any | None, dict[str, Any]]:
    """Support both tuple-based and legacy single-object load results."""

    if isinstance(load_result, tuple) and len(load_result) == 2:
        classifier, metadata = load_result
        if isinstance(metadata, dict):
            return classifier, dict(metadata)

    if load_result is None:
        return None, dict(_TEXT_RUNTIME_STATUS)

    return load_result, dict(_TEXT_RUNTIME_STATUS)


def map_model_outputs_to_project_emotions(raw_output) -> dict[str, float]:
    """Map transformer emotion outputs into the seven-emotion project schema.

    The project schema is fixed to:
    ``["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]``.

    The helper accepts common Hugging Face pipeline output shapes, including a
    single ``{"label": ..., "score": ...}`` record, a list of records, or the
    nested list form emitted by ``top_k=None``. Broader emotion labels such as
    ``love``, ``optimism``, ``gratitude``, ``approval``, ``curiosity``, and
    ``relief`` are mapped into the closest project emotion before the
    distribution is renormalized.
    """

    mapped = {emotion: 0.0 for emotion in EMOTIONS}
    unknown_mass = 0.0

    for record in _flatten_pipeline_output(raw_output):
        label = _normalize_model_label(record.get("label"))
        score = max(0.0, float(record.get("score", 0.0)))
        if score <= 0:
            continue

        project_emotion = _project_emotion_for_label(label)
        if project_emotion is None:
            unknown_mass += score
            continue

        mapped[project_emotion] += score

    if unknown_mass > 0:
        mapped["neutral"] += unknown_mass

    if sum(mapped.values()) <= 0:
        mapped["neutral"] = 1.0

    return normalize_probs(mapped)


def detect_text_emotion_rule_based(text: str) -> dict[str, float]:
    """Estimate text emotion probabilities with deterministic lexical fallback.

    This path is intentionally conservative. It is only meant to recover a
    usable seven-class distribution when transformer loading or inference is
    unavailable. The detector uses small keyword banks, light neutral hints,
    and a few punctuation cues so that repeated demos remain predictable. It
    does not mutate the runtime status; the caller owns any status updates.
    """

    normalized_text = _clean_text(text)
    raw_text = text or ""
    scores = {emotion: 0.35 for emotion in EMOTIONS}
    scores["neutral"] = 1.0

    matched_any = False
    for emotion, keyword_bank in _KEYWORD_BANKS.items():
        for term, weight in keyword_bank.items():
            hits = _count_term(term, normalized_text)
            if hits:
                matched_any = True
                scores[emotion] += weight * hits

    neutral_hits = sum(_count_term(term, normalized_text) for term in _NEUTRAL_HINTS)
    if neutral_hits:
        matched_any = True
        scores["neutral"] += 1.3 * neutral_hits
        scores["sad"] += 0.2 * neutral_hits

    exclamation_count = min(raw_text.count("!"), 3)
    if exclamation_count:
        scores["happy"] += 0.15 * exclamation_count
        scores["angry"] += 0.12 * exclamation_count
        scores["surprise"] += 0.18 * exclamation_count

    question_count = min(raw_text.count("?"), 3)
    if question_count:
        scores["surprise"] += 0.15 * question_count
        scores["fear"] += 0.12 * question_count
        scores["neutral"] += 0.05 * question_count

    if matched_any:
        scores["neutral"] += 0.5
    else:
        scores["neutral"] += 5.0

    return normalize_scores(scores)


def detect_text_emotion(text: str) -> dict[str, float]:
    """Detect text emotion with the transformer runtime first.

    The function attempts to use the Hugging Face transformer pipeline on every
    call. If loading or inference fails for any reason, it falls back to the
    deterministic lexical detector and returns the same seven-class schema.
    """

    load_result = load_text_emotion_pipeline()
    classifier, metadata = _coerce_loaded_runtime(load_result)

    if classifier is not None:
        try:
            raw_output = classifier(text or "", truncation=True)
            mapped = map_model_outputs_to_project_emotions(raw_output)
            success_status = dict(metadata)
            success_status.update(
                {
                    "runtime_mode": "transformer",
                    "transformer_active": True,
                    "fallback_used": False,
                    "message": (
                        "Transformer runtime is active. "
                        f"Loaded {_TEXT_MODEL_NAME} for text emotion inference."
                    ),
                }
            )
            _set_runtime_status(success_status)
            return mapped
        except Exception as exc:
            fallback_status = dict(metadata)
            fallback_status.update(
                {
                    "runtime_mode": "transformer",
                    "transformer_active": True,
                    "fallback_used": True,
                    "message": (
                        "Transformer inference failed for this input. "
                        "Using the emergency rule-based fallback."
                    ),
                    "inference_error": _short_error_message(exc),
                }
            )
            _set_runtime_status(fallback_status)
            return detect_text_emotion_rule_based(text)

    _set_runtime_status(metadata)
    return detect_text_emotion_rule_based(text)

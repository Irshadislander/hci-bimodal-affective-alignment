"""Transformer-first text emotion detection with rule-based fallback."""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

try:
    from app.utils import normalize_probs
except ImportError:  # pragma: no cover - supports running from app/ directly
    from utils import normalize_probs

EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]

_TEXT_MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

_TEXT_BACKEND_STATUS = {
    "mode": "uninitialized",
    "message": "Text emotion backend not initialized.",
}

_MODEL_LABEL_TO_PROJECT = {
    "anger": "angry",
    "annoyance": "angry",
    "disapproval": "angry",
    "frustration": "angry",
    "disgust": "disgust",
    "fear": "fear",
    "nervousness": "fear",
    "anxiety": "fear",
    "joy": "happy",
    "joyful": "happy",
    "happiness": "happy",
    "happy": "happy",
    "love": "happy",
    "optimism": "happy",
    "gratitude": "happy",
    "admiration": "happy",
    "amusement": "happy",
    "caring": "happy",
    "excitement": "happy",
    "relief": "happy",
    "pride": "happy",
    "sadness": "sad",
    "sad": "sad",
    "grief": "sad",
    "disappointment": "sad",
    "remorse": "sad",
    "embarrassment": "sad",
    "neutral": "neutral",
    "surprise": "surprise",
    "astonishment": "surprise",
    "realization": "surprise",
    "confusion": "neutral",
    "approval": "happy",
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
        "relieved": 1.2,
        "joy": 1.8,
        "wonderful": 2.1,
        "love it": 1.7,
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
        "not okay": 2.0,
        "not good": 1.8,
        "feeling low": 1.6,
        "rough day": 1.4,
    },
    "angry": {
        "angry": 2.3,
        "mad": 2.0,
        "frustrated": 2.1,
        "annoyed": 1.5,
        "furious": 2.3,
        "irritated": 1.7,
        "fed up": 1.9,
        "bothered": 1.2,
        "rage": 2.2,
        "resentful": 1.5,
        "stressed": 1.1,
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
}


def _set_backend_status(mode: str, message: str) -> None:
    """Store the active text emotion backend status for the UI."""

    global _TEXT_BACKEND_STATUS
    _TEXT_BACKEND_STATUS = {"mode": mode, "message": message}


def get_text_emotion_backend_status() -> dict[str, str]:
    """Return the current text emotion backend status."""

    return dict(_TEXT_BACKEND_STATUS)


def normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    """Normalize raw emotion scores into a probability distribution."""

    aligned = {emotion: float(scores.get(emotion, 0.0)) for emotion in EMOTIONS}
    return normalize_probs(aligned)


def _count_term(term: str, text_lower: str) -> int:
    """Count exact term matches in the normalized text string."""

    pattern = rf"\b{re.escape(term)}\b"
    return len(re.findall(pattern, text_lower))


@lru_cache(maxsize=1)
def load_text_emotion_pipeline():
    """Load and cache the pretrained HuggingFace text emotion pipeline."""

    try:
        from transformers import pipeline
    except Exception:
        _set_backend_status(
            "rule-based fallback",
            "Transformers is unavailable. Using rule-based text emotion fallback.",
        )
        return None

    try:
        classifier = pipeline(
            "text-classification",
            model=_TEXT_MODEL_NAME,
            tokenizer=_TEXT_MODEL_NAME,
            top_k=None,
            device=-1,
        )
    except Exception:
        _set_backend_status(
            "rule-based fallback",
            "Transformer text model could not be loaded. Using rule-based text emotion fallback.",
        )
        return None

    _set_backend_status(
        "transformer",
        "Using pretrained transformer-based text emotion module.",
    )
    return classifier


def _flatten_pipeline_output(raw_output: Any) -> list[dict[str, Any]]:
    """Flatten common HuggingFace pipeline output shapes into records."""

    if raw_output is None:
        return []

    if isinstance(raw_output, dict):
        if "label" in raw_output and "score" in raw_output:
            return [raw_output]
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


def map_model_outputs_to_project_emotions(raw_output) -> dict[str, float]:
    """Map transformer outputs into the seven-emotion project schema."""

    mapped = {emotion: 0.0 for emotion in EMOTIONS}
    unknown_mass = 0.0

    for record in _flatten_pipeline_output(raw_output):
        label = str(record.get("label", "")).strip().lower()
        label = label.replace(" ", "_").replace("-", "_")
        score = max(0.0, float(record.get("score", 0.0)))
        project_emotion = _MODEL_LABEL_TO_PROJECT.get(label)
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
    """Estimate emotion probabilities from text using lexical heuristics."""

    _set_backend_status(
        "rule-based fallback",
        "Using rule-based text emotion fallback.",
    )

    normalized_text = " ".join(re.findall(r"[a-z']+", (text or "").lower()))
    scores = {emotion: 0.4 for emotion in EMOTIONS}
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
        scores["neutral"] += 1.4 * neutral_hits
        scores["sad"] += 0.3 * neutral_hits

    if matched_any:
        scores["neutral"] += 0.5
    else:
        scores["neutral"] += 5.0

    return normalize_scores(scores)


def detect_text_emotion(text: str) -> dict[str, float]:
    """Detect text emotion with a pretrained transformer or safe fallback."""

    classifier = load_text_emotion_pipeline()
    if classifier is not None:
        try:
            raw_output = classifier(text or "", truncation=True)
            mapped = map_model_outputs_to_project_emotions(raw_output)
            _set_backend_status(
                "transformer",
                "Using pretrained transformer-based text emotion module.",
            )
            return mapped
        except Exception:
            _set_backend_status(
                "rule-based fallback",
                "Transformer text analysis failed. Using rule-based text emotion fallback.",
            )

    return detect_text_emotion_rule_based(text)

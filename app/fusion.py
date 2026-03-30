"""Weighted fusion utilities for combining text and face emotions."""

from __future__ import annotations

try:
    from app.text_emotion import EMOTIONS
except ImportError:  # pragma: no cover - supports running from app/ directly
    from text_emotion import EMOTIONS


def _aligned_probs(probs: dict[str, float]) -> dict[str, float]:
    """Return a probability dict aligned to the starter emotion order."""

    return {emotion: float(probs.get(emotion, 0.0)) for emotion in EMOTIONS}


def fuse_emotions(
    text_probs: dict[str, float],
    face_probs: dict[str, float],
    alpha: float,
) -> tuple[dict[str, float], str]:
    """Fuse text and face predictions with a weighted average."""

    alpha = max(0.0, min(1.0, float(alpha)))
    text_probs = _aligned_probs(text_probs)
    face_probs = _aligned_probs(face_probs)

    fused_probs = {
        emotion: alpha * text_probs[emotion] + (1.0 - alpha) * face_probs[emotion]
        for emotion in EMOTIONS
    }
    top_emotion = max(EMOTIONS, key=lambda emotion: fused_probs[emotion])
    return fused_probs, top_emotion

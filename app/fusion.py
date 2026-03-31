"""Weighted fusion utilities for combining text and face emotions.

The prototype uses a simple convex combination: `alpha` controls how much
weight is assigned to the text modality, while `1 - alpha` controls the face
modality. This keeps the fusion step transparent for research-style demos.
"""

from __future__ import annotations

try:
    from app.text_emotion import EMOTIONS
except ImportError:  # pragma: no cover - supports running from app/ directly
    from text_emotion import EMOTIONS


def _aligned_probs(probs: dict[str, float]) -> dict[str, float]:
    """Return a probability dict aligned to the project emotion order."""

    return {emotion: float(probs.get(emotion, 0.0)) for emotion in EMOTIONS}


def get_top_n_emotions(probs: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the top `n` emotions sorted from highest to lowest probability."""

    n = max(0, int(n))
    sorted_items = sorted(probs.items(), key=lambda item: (-item[1], item[0]))
    return [(emotion, float(probability)) for emotion, probability in sorted_items[:n]]


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
    top_emotion = get_top_n_emotions(fused_probs, n=1)[0][0]
    return fused_probs, top_emotion

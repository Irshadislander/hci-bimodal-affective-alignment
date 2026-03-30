"""Mock facial emotion detection for the Day 1 starter demo."""

from __future__ import annotations

try:
    from app.text_emotion import EMOTIONS
except ImportError:  # pragma: no cover - supports running from app/ directly
    from text_emotion import EMOTIONS


def detect_face_emotion() -> dict[str, float]:
    """Return a deterministic mock probability distribution for face emotion."""

    values = [0.16, 0.07, 0.05, 0.48, 0.05, 0.12, 0.07]
    return dict(zip(EMOTIONS, values, strict=True))

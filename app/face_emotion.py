"""Mock facial emotion detection for the Day 2 prototype."""

from __future__ import annotations

import random

try:
    from app.text_emotion import EMOTIONS
except ImportError:  # pragma: no cover - supports running from app/ directly
    from text_emotion import EMOTIONS


def _profile(values: list[float]) -> dict[str, float]:
    """Build an emotion profile aligned to the shared emotion order."""

    return dict(zip(EMOTIONS, values, strict=True))


_MOCK_FACE_PROFILES = [
    _profile([0.56, 0.06, 0.04, 0.19, 0.03, 0.08, 0.04]),
    _profile([0.11, 0.09, 0.05, 0.55, 0.07, 0.09, 0.04]),
    _profile([0.08, 0.16, 0.29, 0.22, 0.10, 0.07, 0.08]),
    _profile([0.09, 0.14, 0.34, 0.20, 0.08, 0.05, 0.10]),
    _profile([0.09, 0.36, 0.07, 0.24, 0.10, 0.05, 0.09]),
]


def get_mock_face_profiles() -> list[dict[str, float]]:
    """Return the available mock facial emotion profiles."""

    return [profile.copy() for profile in _MOCK_FACE_PROFILES]


def detect_face_emotion() -> dict[str, float]:
    """Return one of several realistic mock facial emotion profiles."""

    profile = random.choice(get_mock_face_profiles())
    return profile.copy()

"""Small shared utilities for the starter demo."""

from __future__ import annotations


def pretty_probs(probs: dict[str, float]) -> dict[str, float]:
    """Round probabilities to three decimal places for display."""

    return {emotion: round(value, 3) for emotion, value in probs.items()}

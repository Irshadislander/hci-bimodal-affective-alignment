"""Small shared utilities for the prototype demo."""

from __future__ import annotations

import pandas as pd


def pretty_probs(probs: dict[str, float]) -> dict[str, float]:
    """Round probabilities to three decimal places for display."""

    return {emotion: round(float(value), 3) for emotion, value in probs.items()}


def sort_probs(probs: dict[str, float]) -> dict[str, float]:
    """Return probabilities sorted from highest to lowest."""

    return dict(
        sorted(
            ((emotion, float(value)) for emotion, value in probs.items()),
            key=lambda item: (-item[1], item[0]),
        )
    )


def probs_to_dataframe(probs: dict[str, float]) -> pd.DataFrame:
    """Convert a probability dictionary into a clean pandas DataFrame."""

    rows = [
        {"Emotion": emotion.title(), "Probability": round(float(value), 3)}
        for emotion, value in sort_probs(probs).items()
    ]
    frame = pd.DataFrame(rows)
    if frame.empty:
        return pd.DataFrame(columns=["Probability"]).rename_axis("Emotion")
    return frame.set_index("Emotion")

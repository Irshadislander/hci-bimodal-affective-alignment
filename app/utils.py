"""Small shared utilities for the prototype demo."""

from __future__ import annotations


def pretty_probs(probs: dict[str, float]) -> dict[str, float]:
    """Round probabilities to three decimal places for display."""

    return {emotion: round(float(value), 3) for emotion, value in probs.items()}


def normalize_probs(probs: dict[str, float]) -> dict[str, float]:
    """Normalize a probability-like dictionary to sum to 1.0.

    If the input is empty, the function returns an empty dictionary. If the
    total score is zero, values are spread uniformly across the existing keys.
    """

    cleaned = {emotion: max(0.0, float(value)) for emotion, value in probs.items()}
    if not cleaned:
        return {}

    total = sum(cleaned.values())
    if total <= 0:
        uniform = 1.0 / len(cleaned)
        return {emotion: uniform for emotion in cleaned}

    return {emotion: value / total for emotion, value in cleaned.items()}


def sort_probs(probs: dict[str, float]) -> dict[str, float]:
    """Return probabilities sorted from highest to lowest."""

    return dict(
        sorted(
            ((emotion, float(value)) for emotion, value in probs.items()),
            key=lambda item: (-item[1], item[0]),
        )
    )


def probs_to_dataframe(probs: dict[str, float]) -> object:
    """Convert a probability dictionary into a display-friendly table.

    Returns a pandas DataFrame when pandas is available, otherwise returns a
    list of row dictionaries that Streamlit can still render.
    """

    rows = [
        {"Emotion": emotion.title(), "Probability": round(float(value), 3)}
        for emotion, value in sort_probs(probs).items()
    ]
    try:
        import pandas as pd
    except Exception:
        return rows

    frame = pd.DataFrame(rows)
    if frame.empty:
        return pd.DataFrame(columns=["Probability"]).rename_axis("Emotion")
    return frame.set_index("Emotion")

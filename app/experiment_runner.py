"""Batch evaluation utilities for ablation and alpha sensitivity studies."""

from __future__ import annotations

import csv
from pathlib import Path

try:  # pragma: no cover - optional dependency
    import pandas as pd
except Exception:  # pragma: no cover - keep the prototype runnable without pandas
    pd = None  # type: ignore[assignment]

try:
    from app.evaluation import evaluate_case
    from app.text_emotion import detect_text_emotion
except ImportError:  # pragma: no cover - supports running from app/ directly
    from evaluation import evaluate_case
    from text_emotion import detect_text_emotion

DEFAULT_CASES = [
    "I am really happy with how this turned out.",
    "Today felt rough and I am still sad about it.",
    "I am frustrated because the system keeps failing.",
    "I feel okay, just checking in for now.",
    "I am nervous about the presentation tomorrow.",
    "Wow, I did not expect that result at all.",
    "That smelled gross and made me uncomfortable.",
    "I am excited and relieved after finishing the task.",
    "It is a mixed day: part of me feels hopeful, part of me feels tired.",
    "I am angry, but also a little worried about what comes next.",
    "The meeting was fine and nothing unusual happened.",
    "I feel a bit disappointed, but I can recover from it.",
]

DEFAULT_ALPHA_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]

BASE_DIR = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = BASE_DIR / "experiments"
ABLATION_RESULTS_PATH = EXPERIMENTS_DIR / "ablation_results.csv"
ALPHA_SENSITIVITY_PATH = EXPERIMENTS_DIR / "alpha_sensitivity.csv"

_OFFLINE_FACE_PROBS = {
    "happy": 0.08,
    "sad": 0.08,
    "angry": 0.05,
    "neutral": 0.62,
    "fear": 0.06,
    "surprise": 0.06,
    "disgust": 0.05,
}


def _save_dataframe(df: pd.DataFrame, path: Path) -> pd.DataFrame:
    """Persist a tabular result to CSV and return it unchanged."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if pd is not None and isinstance(df, pd.DataFrame):
        df.to_csv(path, index=False)
        return df

    rows = list(df)
    if rows:
        fieldnames = list(rows[0].keys())
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        path.write_text("", encoding="utf-8")
    return df


def _row_from_case(case_index: int, user_text: str, alpha: float) -> dict[str, object]:
    """Evaluate one case and flatten the most useful comparison fields."""

    text_probs = detect_text_emotion(user_text)
    face_probs = dict(_OFFLINE_FACE_PROBS)
    case = evaluate_case(user_text, text_probs, face_probs, alpha)
    return {
        "case_id": case_index,
        "user_text": case["user_text"],
        "alpha": case["alpha"],
        "text_top_emotion": case["text_top_emotion"],
        "text_top_probability": case["text_top_probability"],
        "face_top_emotion": case["face_top_emotion"],
        "face_top_probability": case["face_top_probability"],
        "fused_top_emotion": case["fused_top_emotion"],
        "fused_top_probability": case["fused_top_probability"],
        "text_only_top_emotion": case["text_only_top_emotion"],
        "face_only_top_emotion": case["face_only_top_emotion"],
        "empathetic_response": case["empathetic_response"],
    }


def run_ablation_study(alpha: float = 0.5) -> pd.DataFrame:
    """Run a fixed-alpha ablation study over the default case set."""

    rows = [
        _row_from_case(case_index, user_text, alpha)
        for case_index, user_text in enumerate(DEFAULT_CASES, start=1)
    ]
    df = pd.DataFrame(rows) if pd is not None else rows
    return _save_dataframe(df, ABLATION_RESULTS_PATH)


def run_alpha_sensitivity(alphas: list[float]) -> pd.DataFrame:
    """Run the default cases over a grid of alpha values."""

    alpha_values = [float(alpha) for alpha in (alphas or DEFAULT_ALPHA_GRID)]
    rows = []
    for alpha in alpha_values:
        for case_index, user_text in enumerate(DEFAULT_CASES, start=1):
            rows.append(_row_from_case(case_index, user_text, alpha))
    df = pd.DataFrame(rows) if pd is not None else rows
    return _save_dataframe(df, ALPHA_SENSITIVITY_PATH)

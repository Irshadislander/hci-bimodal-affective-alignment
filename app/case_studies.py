"""Case-study generation helpers for the Day 7 prototype."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

try:  # pragma: no cover - optional dependency
    import pandas as pd
except Exception:  # pragma: no cover - keep the prototype runnable without pandas
    pd = None  # type: ignore[assignment]

try:
    from app.evaluation import evaluate_case
    from app.text_emotion import detect_text_emotion
    from app.utils import normalize_probs
except ImportError:  # pragma: no cover - supports running from app/ directly
    from evaluation import evaluate_case
    from text_emotion import detect_text_emotion
    from utils import normalize_probs


BASE_DIR = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = BASE_DIR / "experiments"
CASE_STUDIES_OUTPUT_PATH = EXPERIMENTS_DIR / "case_studies.csv"


_FACE_PROFILES_RAW = {
    "happy": {
        "happy": 0.68,
        "sad": 0.04,
        "angry": 0.04,
        "neutral": 0.12,
        "fear": 0.04,
        "surprise": 0.05,
        "disgust": 0.03,
    },
    "sad": {
        "happy": 0.04,
        "sad": 0.68,
        "angry": 0.05,
        "neutral": 0.12,
        "fear": 0.05,
        "surprise": 0.03,
        "disgust": 0.03,
    },
    "angry": {
        "happy": 0.04,
        "sad": 0.06,
        "angry": 0.66,
        "neutral": 0.12,
        "fear": 0.05,
        "surprise": 0.03,
        "disgust": 0.04,
    },
    "fear": {
        "happy": 0.04,
        "sad": 0.06,
        "angry": 0.04,
        "neutral": 0.12,
        "fear": 0.66,
        "surprise": 0.05,
        "disgust": 0.03,
    },
    "surprise": {
        "happy": 0.08,
        "sad": 0.04,
        "angry": 0.03,
        "neutral": 0.14,
        "fear": 0.05,
        "surprise": 0.64,
        "disgust": 0.02,
    },
    "neutral": {
        "happy": 0.09,
        "sad": 0.08,
        "angry": 0.05,
        "neutral": 0.66,
        "fear": 0.05,
        "surprise": 0.04,
        "disgust": 0.03,
    },
    "disgust": {
        "happy": 0.03,
        "sad": 0.06,
        "angry": 0.08,
        "neutral": 0.12,
        "fear": 0.04,
        "surprise": 0.03,
        "disgust": 0.64,
    },
}

_FACE_PROFILES = {
    name: normalize_probs(profile) for name, profile in _FACE_PROFILES_RAW.items()
}

DEFAULT_CASE_STUDIES = [
    {
        "user_text": "I am thrilled with the result and feel genuinely happy.",
        "case_type": "Congruent",
        "face_profile": "happy",
    },
    {
        "user_text": "I feel sad and drained after losing the opportunity.",
        "case_type": "Congruent",
        "face_profile": "sad",
    },
    {
        "user_text": "I am furious that the system keeps crashing.",
        "case_type": "Congruent",
        "face_profile": "angry",
    },
    {
        "user_text": "I am nervous about the interview tomorrow.",
        "case_type": "Congruent",
        "face_profile": "fear",
    },
    {
        "user_text": "Wow, I did not expect that announcement at all.",
        "case_type": "Congruent",
        "face_profile": "surprise",
    },
    {
        "user_text": "I am thrilled with the result, but the room felt gloomy to me.",
        "case_type": "Dissonant",
        "face_profile": "sad",
    },
    {
        "user_text": "I feel sad and drained after losing the opportunity, even though everyone looks upbeat.",
        "case_type": "Dissonant",
        "face_profile": "happy",
    },
    {
        "user_text": "I am angry about the delay, but the room feels calm and neutral.",
        "case_type": "Dissonant",
        "face_profile": "neutral",
    },
    {
        "user_text": "I am okay, just checking in and moving through the day.",
        "case_type": "Ambiguous",
        "face_profile": "neutral",
    },
    {
        "user_text": "Part of me feels hopeful, part of me feels tired.",
        "case_type": "Ambiguous",
        "face_profile": "neutral",
    },
]


def _table_rows(table: Any) -> list[dict[str, Any]]:
    """Convert a table-like object into a list of row dictionaries."""

    if pd is not None and isinstance(table, pd.DataFrame):
        return table.to_dict(orient="records")
    if isinstance(table, list):
        return [dict(row) for row in table]
    if hasattr(table, "to_dict"):
        try:
            return list(table.to_dict(orient="records"))
        except Exception:
            pass
    return [dict(row) for row in table]


def _build_table(rows: list[dict[str, Any]]) -> object:
    """Build a display-friendly table object from case-study rows."""

    if pd is not None:
        return pd.DataFrame(rows)
    return rows


def _save_table(table: object, path: str | Path) -> str:
    """Save a table-like object to CSV and return the written path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if pd is not None and isinstance(table, pd.DataFrame):
        table.to_csv(output_path, index=False)
        return str(output_path)

    rows = _table_rows(table)
    if rows:
        fieldnames = list(rows[0].keys())
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        output_path.write_text("", encoding="utf-8")
    return str(output_path)


def _build_case_row(case_id: int, case_spec: dict[str, Any], alpha: float) -> dict[str, Any]:
    """Evaluate one case-study example and build the final table row."""

    user_text = str(case_spec.get("user_text", "")).strip()
    case_type = str(case_spec.get("case_type", "Ambiguous"))
    face_profile = str(case_spec.get("face_profile", "neutral"))
    face_probs = dict(_FACE_PROFILES.get(face_profile, _FACE_PROFILES["neutral"]))
    text_probs = detect_text_emotion(user_text)
    case = evaluate_case(user_text, text_probs, face_probs, alpha)

    return {
        "case_id": case_id,
        "user_text": case["user_text"],
        "text_top_emotion": case["text_top_emotion"],
        "face_top_emotion": case["face_top_emotion"],
        "fused_top_emotion": case["fused_top_emotion"],
        "empathetic_response": case["empathetic_response"],
        "case_type": case_type,
    }


def generate_case_study_table(alpha: float = 0.5) -> object:
    """Generate a compact case-study table for the report and slides."""

    rows = [
        _build_case_row(case_id, case_spec, alpha)
        for case_id, case_spec in enumerate(DEFAULT_CASE_STUDIES, start=1)
    ]
    table = _build_table(rows)
    _save_table(table, CASE_STUDIES_OUTPUT_PATH)
    return table

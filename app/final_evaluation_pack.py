"""Final human-evaluation and comparison assets for the project."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_SITE_PACKAGES = ROOT / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
if VENV_SITE_PACKAGES.exists() and str(VENV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(VENV_SITE_PACKAGES))

import pandas as pd

try:
    from app.case_studies import DEFAULT_CASE_STUDIES
    from app.fusion import fuse_emotions, get_top_n_emotions
    from app.response_generator import generate_response
    from app.text_emotion import detect_text_emotion
    from app.utils import normalize_probs
except ImportError:  # pragma: no cover - supports running from app/ directly
    from case_studies import DEFAULT_CASE_STUDIES
    from fusion import fuse_emotions, get_top_n_emotions
    from response_generator import generate_response
    from text_emotion import detect_text_emotion
    from utils import normalize_probs

EXPERIMENTS_DIR = ROOT / "experiments"
MODE_COMPARISON_CASES_PATH = EXPERIMENTS_DIR / "mode_comparison_cases.csv"
HUMAN_RATING_SHEET_PATH = EXPERIMENTS_DIR / "human_rating_sheet.csv"
HUMAN_RATING_SHEET_COMPLETED_PATH = EXPERIMENTS_DIR / "human_rating_sheet_completed.csv"
HUMAN_EVAL_SUMMARY_PATH = EXPERIMENTS_DIR / "human_eval_summary.csv"

MODE_ORDER = ["text_only", "face_only", "fused"]
MODE_DISPLAY_LABELS = {
    "text_only": "Text only",
    "face_only": "Face only",
    "fused": "Fused",
}
RATING_COLUMNS = [
    "empathy_rating",
    "social_presence_rating",
    "trust_rating",
    "helpfulness_rating",
]
RATING_SHEET_COLUMNS = [
    "rater_id",
    "case_id",
    "case_type",
    "user_text",
    "mode",
    "detected_emotion",
    "system_response",
    "empathy_rating",
    "social_presence_rating",
    "trust_rating",
    "helpfulness_rating",
    "notes",
]

_FACE_PROFILES_RAW = {
    "happy": {
        "happy": 0.70,
        "sad": 0.04,
        "angry": 0.04,
        "neutral": 0.11,
        "fear": 0.03,
        "surprise": 0.05,
        "disgust": 0.03,
    },
    "sad": {
        "happy": 0.04,
        "sad": 0.70,
        "angry": 0.04,
        "neutral": 0.11,
        "fear": 0.05,
        "surprise": 0.03,
        "disgust": 0.03,
    },
    "angry": {
        "happy": 0.04,
        "sad": 0.05,
        "angry": 0.68,
        "neutral": 0.10,
        "fear": 0.05,
        "surprise": 0.04,
        "disgust": 0.04,
    },
    "fear": {
        "happy": 0.04,
        "sad": 0.05,
        "angry": 0.04,
        "neutral": 0.10,
        "fear": 0.67,
        "surprise": 0.06,
        "disgust": 0.04,
    },
    "surprise": {
        "happy": 0.07,
        "sad": 0.04,
        "angry": 0.03,
        "neutral": 0.12,
        "fear": 0.05,
        "surprise": 0.66,
        "disgust": 0.03,
    },
    "neutral": {
        "happy": 0.08,
        "sad": 0.08,
        "angry": 0.05,
        "neutral": 0.66,
        "fear": 0.05,
        "surprise": 0.05,
        "disgust": 0.03,
    },
    "disgust": {
        "happy": 0.03,
        "sad": 0.05,
        "angry": 0.07,
        "neutral": 0.11,
        "fear": 0.04,
        "surprise": 0.03,
        "disgust": 0.67,
    },
}

_FACE_PROFILES = {
    name: normalize_probs(profile) for name, profile in _FACE_PROFILES_RAW.items()
}


def _ensure_parent(path: str | Path) -> Path:
    """Create the parent directory for a path and return the path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def _top_emotion(probs: dict[str, float]) -> str:
    """Return the top emotion label from a probability dictionary."""

    top = get_top_n_emotions(probs, n=1)
    return top[0][0] if top else "neutral"


def _normalize_mode_value(value: object) -> str:
    """Normalize a mode label to the internal comparison schema."""

    mode = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    if mode in MODE_ORDER:
        return mode
    for key, label in MODE_DISPLAY_LABELS.items():
        if mode == label.lower().replace(" ", "_"):
            return key
    return mode


def _face_probs_from_case(case_spec: dict[str, object]) -> dict[str, float]:
    """Return a stable facial probability profile for a case study example."""

    profile_name = str(case_spec.get("face_profile", "neutral"))
    return dict(_FACE_PROFILES.get(profile_name, _FACE_PROFILES["neutral"]))


def _response_for_mode(user_text: str, emotion: str, mode: str) -> str:
    """Generate a stable response variant for a specific comparison mode."""

    mode_seed = f"{mode}|{user_text}"
    return generate_response(mode_seed, emotion)


def _mode_rows_for_case(
    case_id: int,
    case_spec: dict[str, object],
    alpha: float,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Build one comparison row and three human-rating rows for a case."""

    user_text = str(case_spec.get("user_text", "")).strip()
    case_type = str(case_spec.get("case_type", "Ambiguous"))
    text_probs = detect_text_emotion(user_text)
    face_probs = _face_probs_from_case(case_spec)
    fused_probs, fused_emotion = fuse_emotions(text_probs, face_probs, alpha)

    text_top_emotion = _top_emotion(text_probs)
    face_top_emotion = _top_emotion(face_probs)
    fused_top_emotion = fused_emotion or _top_emotion(fused_probs)

    comparison_row = {
        "case_id": case_id,
        "user_text": user_text,
        "text_top_emotion": text_top_emotion,
        "face_top_emotion": face_top_emotion,
        "fused_top_emotion": fused_top_emotion,
        "text_only_response": _response_for_mode(user_text, text_top_emotion, "text_only"),
        "face_only_response": _response_for_mode(user_text, face_top_emotion, "face_only"),
        "fused_response": _response_for_mode(user_text, fused_top_emotion, "fused"),
        "case_type": case_type,
    }

    rating_rows = []
    for mode, detected_emotion, system_response in (
        ("text_only", text_top_emotion, comparison_row["text_only_response"]),
        ("face_only", face_top_emotion, comparison_row["face_only_response"]),
        ("fused", fused_top_emotion, comparison_row["fused_response"]),
    ):
        rating_rows.append(
            {
                "rater_id": "",
                "case_id": case_id,
                "case_type": case_type,
                "user_text": user_text,
                "mode": MODE_DISPLAY_LABELS.get(mode, mode.title()),
                "detected_emotion": detected_emotion,
                "system_response": system_response,
                "empathy_rating": "",
                "social_presence_rating": "",
                "trust_rating": "",
                "helpfulness_rating": "",
                "notes": "",
            }
        )

    return comparison_row, rating_rows


def build_mode_comparison_cases(alpha: float = 0.5) -> pd.DataFrame:
    """Build text-only, face-only, and fused responses for the default cases."""

    rows: list[dict[str, object]] = []
    for case_id, case_spec in enumerate(DEFAULT_CASE_STUDIES, start=1):
        comparison_row, _ = _mode_rows_for_case(case_id, case_spec, alpha)
        rows.append(comparison_row)

    df = pd.DataFrame(rows, columns=[
        "case_id",
        "user_text",
        "text_top_emotion",
        "face_top_emotion",
        "fused_top_emotion",
        "text_only_response",
        "face_only_response",
        "fused_response",
        "case_type",
    ])
    df.to_csv(_ensure_parent(MODE_COMPARISON_CASES_PATH), index=False)
    return df


def build_human_rating_sheet(alpha: float = 0.5) -> pd.DataFrame:
    """Convert the comparison cases into a long-form human rating sheet."""

    rows: list[dict[str, object]] = []
    for case_id, case_spec in enumerate(DEFAULT_CASE_STUDIES, start=1):
        _, rating_rows = _mode_rows_for_case(case_id, case_spec, alpha)
        rows.extend(rating_rows)

    df = pd.DataFrame(rows, columns=RATING_SHEET_COLUMNS)
    df.to_csv(_ensure_parent(HUMAN_RATING_SHEET_PATH), index=False)
    return df


def validate_completed_human_ratings(path: str = "experiments/human_rating_sheet_completed.csv") -> dict[str, object]:
    """Validate a completed human-rating file without raising on missing input."""

    rating_path = Path(path)
    report: dict[str, object] = {
        "file_exists": rating_path.exists(),
        "path": str(rating_path),
        "required_columns": list(RATING_SHEET_COLUMNS),
        "missing_columns": [],
        "total_rows": 0,
        "completed_rows": 0,
        "unique_raters": 0,
        "missing_values_by_column": {},
        "missing_values_total": 0,
        "mode_counts": {},
        "status": "missing_file" if not rating_path.exists() else "invalid",
    }

    if not rating_path.exists():
        report["missing_columns"] = list(RATING_SHEET_COLUMNS)
        return report

    try:
        df = pd.read_csv(rating_path)
    except Exception as exc:
        report["status"] = "read_error"
        report["error"] = str(exc)
        report["missing_columns"] = list(RATING_SHEET_COLUMNS)
        return report

    missing_columns = [column for column in RATING_SHEET_COLUMNS if column not in df.columns]
    report["missing_columns"] = missing_columns
    report["total_rows"] = int(len(df))

    if "rater_id" in df.columns:
        report["unique_raters"] = int(df["rater_id"].replace("", pd.NA).dropna().nunique())
    if "mode" in df.columns:
        normalized_modes = df["mode"].replace("", pd.NA).dropna().map(_normalize_mode_value)
        mode_counts = normalized_modes.value_counts()
        report["mode_counts"] = {str(key): int(value) for key, value in mode_counts.items()}

    missing_values_by_column: dict[str, int] = {}
    for column in RATING_SHEET_COLUMNS:
        if column in df.columns:
            missing_values_by_column[column] = int(df[column].replace("", pd.NA).isna().sum())
        else:
            missing_values_by_column[column] = int(len(df))
    report["missing_values_by_column"] = missing_values_by_column
    report["missing_values_total"] = int(sum(missing_values_by_column.values()))

    if all(column in df.columns for column in RATING_COLUMNS):
        complete_mask = (
            df[RATING_COLUMNS]
            .replace("", pd.NA)
            .notna()
            .all(axis=1)
        )
        report["completed_rows"] = int(complete_mask.sum())
        report["status"] = "valid" if not missing_columns else "partial"
    else:
        report["status"] = "partial"

    return report


def aggregate_human_ratings(path: str = "experiments/human_rating_sheet_completed.csv") -> tuple[dict[str, object], pd.DataFrame]:
    """Aggregate completed human ratings by mode and save the summary table."""

    output_path = _ensure_parent(HUMAN_EVAL_SUMMARY_PATH)
    rating_path = Path(path)
    summary_columns = [
        "mode",
        "completed_rows",
        "empathy_rating_mean",
        "social_presence_rating_mean",
        "trust_rating_mean",
        "helpfulness_rating_mean",
    ]

    if not rating_path.exists():
        empty_df = pd.DataFrame(columns=summary_columns)
        empty_df.to_csv(output_path, index=False)
        summary_dict = {
            "status": "missing_file",
            "file_exists": False,
            "completed_rows": 0,
            "unique_raters": 0,
            "mode_counts": {},
            "mode_averages": {},
            "summary_path": str(output_path),
        }
        return summary_dict, empty_df

    try:
        df = pd.read_csv(rating_path)
    except Exception as exc:
        empty_df = pd.DataFrame(columns=summary_columns)
        empty_df.to_csv(output_path, index=False)
        summary_dict = {
            "status": "read_error",
            "file_exists": True,
            "error": str(exc),
            "completed_rows": 0,
            "unique_raters": 0,
            "mode_counts": {},
            "mode_averages": {},
            "summary_path": str(output_path),
        }
        return summary_dict, empty_df

    validation = validate_completed_human_ratings(path)
    if validation["missing_columns"]:
        empty_df = pd.DataFrame(columns=summary_columns)
        empty_df.to_csv(output_path, index=False)
        summary_dict = {
            "status": "invalid",
            "file_exists": True,
            "missing_columns": validation["missing_columns"],
            "completed_rows": int(validation["completed_rows"]),
            "unique_raters": int(validation["unique_raters"]),
            "mode_counts": validation["mode_counts"],
            "mode_averages": {},
            "summary_path": str(output_path),
        }
        return summary_dict, empty_df

    working = df.copy()
    for column in RATING_COLUMNS:
        working[column] = pd.to_numeric(working[column], errors="coerce")

    if "mode" not in working.columns:
        empty_df = pd.DataFrame(columns=summary_columns)
        empty_df.to_csv(output_path, index=False)
        summary_dict = {
            "status": "invalid",
            "file_exists": True,
            "completed_rows": int(validation["completed_rows"]),
            "unique_raters": int(validation["unique_raters"]),
            "mode_counts": validation["mode_counts"],
            "mode_averages": {},
            "summary_path": str(output_path),
        }
        return summary_dict, empty_df

    working["mode"] = working["mode"].map(_normalize_mode_value)
    working = working[working["mode"].isin(MODE_ORDER)]

    rows: list[dict[str, object]] = []
    mode_averages: dict[str, dict[str, float]] = {}
    mode_counts: dict[str, int] = {}

    for mode in MODE_ORDER:
        subset = working[working["mode"] == mode].copy()
        mode_counts[mode] = int(len(subset))
        if subset.empty:
            continue

        row = {"mode": mode, "completed_rows": int(len(subset))}
        averages_for_mode: dict[str, float] = {}
        for column in RATING_COLUMNS:
            mean_value = float(subset[column].mean(skipna=True))
            row[f"{column}_mean"] = round(mean_value, 3) if pd.notna(mean_value) else pd.NA
            if pd.notna(mean_value):
                averages_for_mode[column] = round(mean_value, 3)
        rows.append(row)
        mode_averages[mode] = averages_for_mode

    summary_df = pd.DataFrame(rows, columns=summary_columns)
    summary_df.to_csv(output_path, index=False)

    summary_dict = {
        "status": "aggregated",
        "file_exists": True,
        "completed_rows": int(validation["completed_rows"]),
        "unique_raters": int(validation["unique_raters"]),
        "mode_counts": mode_counts,
        "mode_averages": mode_averages,
        "summary_path": str(output_path),
    }
    return summary_dict, summary_df

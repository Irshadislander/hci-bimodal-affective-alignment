"""Report asset loading and summary helpers for the project."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_SITE_PACKAGES = ROOT / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
if VENV_SITE_PACKAGES.exists() and str(VENV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(VENV_SITE_PACKAGES))

import pandas as pd

BASE_DIR = ROOT
EXPERIMENTS_DIR = BASE_DIR / "experiments"

ABLATION_RESULTS_PATH = EXPERIMENTS_DIR / "ablation_results.csv"
ALPHA_RESULTS_PATH = EXPERIMENTS_DIR / "alpha_sensitivity.csv"
CASE_STUDIES_PATH = EXPERIMENTS_DIR / "case_studies.csv"

ABLATION_COLUMNS = [
    "case_id",
    "user_text",
    "alpha",
    "text_top_emotion",
    "text_top_probability",
    "face_top_emotion",
    "face_top_probability",
    "fused_top_emotion",
    "fused_top_probability",
    "text_only_top_emotion",
    "face_only_top_emotion",
    "empathetic_response",
]

CASE_STUDY_COLUMNS = [
    "case_id",
    "user_text",
    "text_top_emotion",
    "face_top_emotion",
    "fused_top_emotion",
    "empathetic_response",
    "case_type",
]


def _empty_dataframe(columns: list[str]) -> pd.DataFrame:
    """Create an empty DataFrame with the expected columns."""

    return pd.DataFrame(columns=columns)


def _read_csv(path: str | Path, columns: list[str]) -> pd.DataFrame:
    """Read a CSV file if available, otherwise return an empty table."""

    csv_path = Path(path)
    if not csv_path.exists():
        return _empty_dataframe(columns)

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return _empty_dataframe(columns)

    for column in columns:
        if column not in df.columns:
            df[column] = pd.NA
    return df


def load_ablation_results(path: str = "experiments/ablation_results.csv") -> pd.DataFrame:
    """Load the saved ablation study results."""

    return _read_csv(path, ABLATION_COLUMNS)


def load_alpha_results(path: str = "experiments/alpha_sensitivity.csv") -> pd.DataFrame:
    """Load the saved alpha sensitivity results."""

    return _read_csv(path, ABLATION_COLUMNS)


def load_case_studies(path: str = "experiments/case_studies.csv") -> pd.DataFrame:
    """Load the saved case-study table."""

    return _read_csv(path, CASE_STUDY_COLUMNS)


def summarize_results_for_report() -> dict[str, object]:
    """Return a compact summary of the generated report assets."""

    ablation_df = load_ablation_results(str(ABLATION_RESULTS_PATH))
    alpha_df = load_alpha_results(str(ALPHA_RESULTS_PATH))
    case_df = load_case_studies(str(CASE_STUDIES_PATH))

    fused_emotions = []
    if "fused_top_emotion" in ablation_df.columns:
        fused_emotions.extend(ablation_df["fused_top_emotion"].dropna().astype(str).tolist())
    if "fused_top_emotion" in case_df.columns:
        fused_emotions.extend(case_df["fused_top_emotion"].dropna().astype(str).tolist())

    alpha_values = []
    if "alpha" in alpha_df.columns:
        alpha_series = pd.to_numeric(alpha_df["alpha"], errors="coerce").dropna()
        alpha_values = sorted({float(value) for value in alpha_series.tolist()})

    case_type_counts: dict[str, int] = {}
    if "case_type" in case_df.columns and not case_df.empty:
        counts = case_df["case_type"].fillna("Unknown").astype(str).value_counts()
        case_type_counts = {str(key): int(value) for key, value in counts.items()}

    summary = {
        "ablation_rows": int(len(ablation_df)),
        "alpha_rows": int(len(alpha_df)),
        "case_study_rows": int(len(case_df)),
        "unique_fused_emotions": sorted(set(fused_emotions)),
        "alpha_values_used": alpha_values,
        "case_type_counts": case_type_counts,
    }
    summary["number_of_cases"] = summary["case_study_rows"] or summary["ablation_rows"]
    return summary

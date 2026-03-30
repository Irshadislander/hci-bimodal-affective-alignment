"""Simple matplotlib plots for report-ready experiment assets."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_SITE_PACKAGES = ROOT / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
if VENV_SITE_PACKAGES.exists() and str(VENV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(VENV_SITE_PACKAGES))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = ROOT
EXPERIMENTS_DIR = BASE_DIR / "experiments"

HUMAN_EVAL_METRICS = [
    "empathy_rating_mean",
    "social_presence_rating_mean",
    "trust_rating_mean",
    "helpfulness_rating_mean",
]
HUMAN_EVAL_SUMMARY_COLUMNS = [
    "mode",
    "completed_rows",
    "empathy_rating_mean",
    "social_presence_rating_mean",
    "trust_rating_mean",
    "helpfulness_rating_mean",
]
MODE_ORDER = ["text_only", "face_only", "fused"]


def _ensure_output_path(output_path: str | Path) -> Path:
    """Create the parent directory for a plot and return the path."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _empty_figure(title: str, message: str):
    """Create a minimal placeholder figure for empty inputs."""

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_title(title)
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12)
    ax.set_axis_off()
    fig.tight_layout()
    return fig, ax


def _finalize_figure(fig, output_path: str | Path) -> str:
    """Save a figure to disk and return the file path."""

    path = _ensure_output_path(output_path)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def _prepare_human_eval_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize human-evaluation data into the expected summary table shape."""

    if df.empty:
        return pd.DataFrame(columns=HUMAN_EVAL_SUMMARY_COLUMNS)

    summary_columns = set(HUMAN_EVAL_SUMMARY_COLUMNS)
    if summary_columns <= set(df.columns):
        summary = df.loc[:, HUMAN_EVAL_SUMMARY_COLUMNS].copy()
        return summary

    if "mode" not in df.columns:
        return pd.DataFrame(columns=HUMAN_EVAL_SUMMARY_COLUMNS)

    metric_sources = {
        "empathy_rating_mean": ["empathy_rating_mean", "empathy_rating"],
        "social_presence_rating_mean": ["social_presence_rating_mean", "social_presence_rating"],
        "trust_rating_mean": ["trust_rating_mean", "trust_rating"],
        "helpfulness_rating_mean": ["helpfulness_rating_mean", "helpfulness_rating"],
    }
    if not any(source in df.columns for sources in metric_sources.values() for source in sources):
        return pd.DataFrame(columns=HUMAN_EVAL_SUMMARY_COLUMNS)

    working = df.copy()
    working["mode"] = working["mode"].astype(str).str.strip()
    working = working[working["mode"] != ""]
    if working.empty:
        return pd.DataFrame(columns=HUMAN_EVAL_SUMMARY_COLUMNS)

    aggregated_rows = []
    for mode, subset in working.groupby("mode"):
        row: dict[str, object] = {"mode": mode, "completed_rows": int(len(subset))}
        for target_column, possible_sources in metric_sources.items():
            source_column = next((column for column in possible_sources if column in subset.columns), None)
            if source_column is None:
                row[target_column] = pd.NA
                continue
            numeric_values = pd.to_numeric(subset[source_column], errors="coerce")
            mean_value = numeric_values.mean(skipna=True)
            row[target_column] = round(float(mean_value), 3) if pd.notna(mean_value) else pd.NA
        aggregated_rows.append(row)

    summary = pd.DataFrame(aggregated_rows, columns=HUMAN_EVAL_SUMMARY_COLUMNS)
    if summary.empty:
        return summary

    summary["mode"] = pd.Categorical(summary["mode"], categories=MODE_ORDER, ordered=True)
    summary = summary.sort_values("mode").reset_index(drop=True)
    summary["mode"] = summary["mode"].astype(str)
    return summary


def plot_ablation_counts(df: pd.DataFrame, output_path: str = "experiments/ablation_counts.png") -> str:
    """Plot fused emotion counts from the ablation study."""

    if df.empty or "fused_top_emotion" not in df.columns:
        fig, ax = _empty_figure("Ablation Study", "No ablation results available yet.")
        return _finalize_figure(fig, output_path)

    counts = df["fused_top_emotion"].fillna("Unknown").astype(str).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    counts.plot(kind="bar", ax=ax, color="#4C72B0")
    ax.set_title("Ablation Study: Fused Emotion Counts")
    ax.set_xlabel("Emotion")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return _finalize_figure(fig, output_path)


def plot_alpha_sensitivity(df: pd.DataFrame, output_path: str = "experiments/alpha_sensitivity_plot.png") -> str:
    """Plot how fused emotions vary across alpha values."""

    required_columns = {"alpha", "fused_top_emotion"}
    if df.empty or not required_columns <= set(df.columns):
        fig, ax = _empty_figure("Alpha Sensitivity", "No alpha sensitivity results available yet.")
        return _finalize_figure(fig, output_path)

    pivot = (
        df.assign(alpha=df["alpha"].astype(float))
        .groupby(["alpha", "fused_top_emotion"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(9, 4.8))
    pivot.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Alpha Sensitivity: Fused Emotion Distribution")
    ax.set_xlabel("Alpha")
    ax.set_ylabel("Case Count")
    ax.legend(title="Emotion", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    return _finalize_figure(fig, output_path)


def plot_case_type_distribution(
    df: pd.DataFrame,
    output_path: str = "experiments/case_type_distribution.png",
) -> str:
    """Plot the distribution of congruent, dissonant, and ambiguous cases."""

    if df.empty or "case_type" not in df.columns:
        fig, ax = _empty_figure("Case Study Types", "No case-study results available yet.")
        return _finalize_figure(fig, output_path)

    counts = df["case_type"].fillna("Unknown").astype(str).value_counts().reindex(
        ["Congruent", "Dissonant", "Ambiguous"], fill_value=0
    )

    fig, ax = plt.subplots(figsize=(7, 4.5))
    counts.plot(kind="bar", ax=ax, color="#55A868")
    ax.set_title("Case Study Type Distribution")
    ax.set_xlabel("Case Type")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    return _finalize_figure(fig, output_path)


def plot_human_eval_summary(
    df: pd.DataFrame,
    output_path: str = "experiments/human_eval_summary_plot.png",
) -> str:
    """Plot average human-evaluation ratings by mode."""

    summary = _prepare_human_eval_summary(df)
    if summary.empty:
        fig, ax = _empty_figure("Human Evaluation Summary", "No completed ratings available yet.")
        return _finalize_figure(fig, output_path)

    plot_df = summary.set_index("mode")[HUMAN_EVAL_METRICS].apply(pd.to_numeric, errors="coerce")
    ordered_modes = [mode for mode in MODE_ORDER if mode in plot_df.index]
    remaining_modes = [mode for mode in plot_df.index if mode not in MODE_ORDER]
    if ordered_modes or remaining_modes:
        plot_df = plot_df.reindex(ordered_modes + remaining_modes)
    if plot_df.empty:
        fig, ax = _empty_figure("Human Evaluation Summary", "No rating means available yet.")
        return _finalize_figure(fig, output_path)

    fig, ax = plt.subplots(figsize=(10, 5))
    plot_df.plot(kind="bar", ax=ax, width=0.82, color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"])
    ax.set_title("Average Human Evaluation Ratings by Mode")
    ax.set_xlabel("Mode")
    ax.set_ylabel("Average rating")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(title="Metric", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    return _finalize_figure(fig, output_path)


def plot_helpfulness_summary(
    df: pd.DataFrame,
    output_path: str = "experiments/helpfulness_summary_plot.png",
) -> str:
    """Plot helpfulness ratings by mode as a compact single-chart summary."""

    summary = _prepare_human_eval_summary(df)
    if summary.empty or "helpfulness_rating_mean" not in summary.columns:
        fig, ax = _empty_figure("Helpfulness Summary", "No helpfulness ratings available yet.")
        return _finalize_figure(fig, output_path)

    plot_df = summary[["mode", "helpfulness_rating_mean"]].copy()
    plot_df["helpfulness_rating_mean"] = pd.to_numeric(plot_df["helpfulness_rating_mean"], errors="coerce")
    plot_df = plot_df.dropna(subset=["helpfulness_rating_mean"])
    plot_df["mode"] = pd.Categorical(plot_df["mode"], categories=MODE_ORDER, ordered=True)
    plot_df = plot_df.sort_values("mode")
    if plot_df.empty:
        fig, ax = _empty_figure("Helpfulness Summary", "No helpfulness means available yet.")
        return _finalize_figure(fig, output_path)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.bar(plot_df["mode"].astype(str), plot_df["helpfulness_rating_mean"], color="#C44E52")
    ax.set_title("Helpfulness Rating by Mode")
    ax.set_xlabel("Mode")
    ax.set_ylabel("Average helpfulness rating")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    return _finalize_figure(fig, output_path)

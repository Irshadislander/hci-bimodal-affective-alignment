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

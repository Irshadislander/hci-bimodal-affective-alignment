"""Final report assembly helpers for the project."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_SITE_PACKAGES = ROOT / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
if VENV_SITE_PACKAGES.exists() and str(VENV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(VENV_SITE_PACKAGES))

import pandas as pd

try:
    import app.final_evaluation_pack as final_pack
    import app.report_assets as report_assets
except ImportError:  # pragma: no cover - supports running from app/ directly
    import final_evaluation_pack as final_pack
    import report_assets

BASE_DIR = ROOT
DOCS_DIR = BASE_DIR / "docs"

REPORT_TABLES_PATH = DOCS_DIR / "report_tables.md"
REPORT_STATUS_PATH = DOCS_DIR / "report_status.md"

MODE_COMPARISON_COLUMNS = [
    "case_id",
    "user_text",
    "text_top_emotion",
    "face_top_emotion",
    "fused_top_emotion",
    "text_only_response",
    "face_only_response",
    "fused_response",
    "case_type",
]

HUMAN_EVAL_SUMMARY_COLUMNS = [
    "mode",
    "completed_rows",
    "empathy_rating_mean",
    "social_presence_rating_mean",
    "trust_rating_mean",
    "helpfulness_rating_mean",
]

SUPPORTED_MODES = ["text_only", "face_only", "fused"]


def _ensure_parent(path: str | Path) -> Path:
    """Create the parent directory for a file path and return the path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def _load_csv(path: str | Path, columns: list[str]) -> pd.DataFrame:
    """Load a CSV file if it exists, otherwise return an empty table."""

    csv_path = Path(path)
    if not csv_path.exists():
        return pd.DataFrame(columns=columns)

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return pd.DataFrame(columns=columns)

    for column in columns:
        if column not in df.columns:
            df[column] = pd.NA
    return df


def _cell_to_text(value: object) -> str:
    """Convert a value into a safe markdown cell string."""

    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    return text


def _display_path(path: str | Path) -> str:
    """Render a repository-relative path when possible."""

    resolved = Path(path)
    try:
        return str(resolved.relative_to(BASE_DIR))
    except Exception:
        return str(resolved)


def _dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Convert a DataFrame into a markdown table without external dependencies."""

    if df.empty:
        return "_No rows available yet._"

    working = df.copy()
    headers = list(working.columns)
    lines = [
        "| " + " | ".join(_cell_to_text(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in working.to_dict(orient="records"):
        lines.append("| " + " | ".join(_cell_to_text(row.get(column, "")) for column in headers) + " |")
    return "\n".join(lines)


def _first_nonempty_length(*frames: pd.DataFrame) -> int:
    """Return the row count from the first non-empty frame, or zero."""

    for frame in frames:
        if not frame.empty:
            if "case_id" in frame.columns:
                non_missing = frame["case_id"].dropna()
                if not non_missing.empty:
                    try:
                        return int(non_missing.nunique())
                    except Exception:
                        pass
            return int(len(frame))
    return 0


def build_report_result_tables() -> dict[str, pd.DataFrame]:
    """Load the current experiment CSVs into a report-friendly dictionary."""

    ablation_table = report_assets.load_ablation_results(str(report_assets.ABLATION_RESULTS_PATH))
    alpha_table = report_assets.load_alpha_results(str(report_assets.ALPHA_RESULTS_PATH))
    case_study_table = report_assets.load_case_studies(str(report_assets.CASE_STUDIES_PATH))
    mode_comparison_table = _load_csv(final_pack.MODE_COMPARISON_CASES_PATH, MODE_COMPARISON_COLUMNS)
    human_eval_summary_table = _load_csv(final_pack.HUMAN_EVAL_SUMMARY_PATH, HUMAN_EVAL_SUMMARY_COLUMNS)

    return {
        "ablation_table": ablation_table,
        "alpha_table": alpha_table,
        "case_study_table": case_study_table,
        "mode_comparison_table": mode_comparison_table,
        "human_eval_summary_table": human_eval_summary_table,
    }


def summarize_for_conclusion() -> dict[str, object]:
    """Return concise conclusion points based on the available experiment files."""

    tables = build_report_result_tables()
    ablation_table = tables["ablation_table"]
    alpha_table = tables["alpha_table"]
    case_study_table = tables["case_study_table"]
    mode_comparison_table = tables["mode_comparison_table"]
    human_eval_summary_table = tables["human_eval_summary_table"]

    number_of_experiment_cases = _first_nonempty_length(
        mode_comparison_table,
        case_study_table,
        ablation_table,
    )
    supported_modes = list(SUPPORTED_MODES)
    has_human_eval_summary = not human_eval_summary_table.empty
    has_case_studies = not case_study_table.empty
    has_alpha_sensitivity = not alpha_table.empty

    summary_points = [
        f"The current evaluation package covers {number_of_experiment_cases} experiment cases.",
        f"Supported comparison modes are {', '.join(supported_modes)}.",
        (
            "A completed human evaluation summary is available."
            if has_human_eval_summary
            else "A completed human evaluation summary is not yet available; collect ratings before final submission."
        ),
        (
            "Case studies are available for congruent, dissonant, and ambiguous examples."
            if has_case_studies
            else "Case studies still need to be generated or restored."
        ),
        (
            "Alpha sensitivity results are available for report discussion."
            if has_alpha_sensitivity
            else "Alpha sensitivity results still need to be generated."
        ),
    ]

    return {
        "number_of_experiment_cases": number_of_experiment_cases,
        "supported_modes": supported_modes,
        "has_human_eval_summary": has_human_eval_summary,
        "has_case_studies": has_case_studies,
        "has_alpha_sensitivity": has_alpha_sensitivity,
        "summary_points": summary_points,
    }


def export_report_tables_markdown(output_path: str = "docs/report_tables.md") -> str:
    """Convert the current result tables into a markdown document."""

    tables = build_report_result_tables()
    sections: list[str] = [
        "# Report Tables",
        "",
        "This document compiles the experiment tables that support the final report.",
        "",
    ]

    table_sections = [
        ("Ablation Table", tables["ablation_table"]),
        ("Alpha Sensitivity Table", tables["alpha_table"]),
        ("Case Study Table", tables["case_study_table"]),
        ("Mode Comparison Table", tables["mode_comparison_table"]),
        ("Human Evaluation Summary Table", tables["human_eval_summary_table"]),
    ]

    for title, df in table_sections:
        sections.append(f"## {title}")
        if df.empty:
            sections.append("_No rows available yet._")
        else:
            sections.append(_dataframe_to_markdown(df))
        sections.append("")

    path = _ensure_parent(output_path)
    path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return str(path)


def export_report_status(output_path: str = "docs/report_status.md") -> str:
    """Write a markdown status report for the final report package."""

    tables = build_report_result_tables()
    summary = summarize_for_conclusion()

    file_rows = [
        ("Experiments", report_assets.ABLATION_RESULTS_PATH, not tables["ablation_table"].empty, "Ablation study results"),
        ("Experiments", report_assets.ALPHA_RESULTS_PATH, not tables["alpha_table"].empty, "Alpha sensitivity results"),
        ("Experiments", report_assets.CASE_STUDIES_PATH, not tables["case_study_table"].empty, "Case study examples"),
        ("Experiments", final_pack.MODE_COMPARISON_CASES_PATH, not tables["mode_comparison_table"].empty, "Mode comparison cases"),
        ("Experiments", final_pack.HUMAN_RATING_SHEET_PATH, Path(final_pack.HUMAN_RATING_SHEET_PATH).exists(), "Blank human rating sheet"),
        ("Experiments", final_pack.HUMAN_RATING_SHEET_COMPLETED_PATH, Path(final_pack.HUMAN_RATING_SHEET_COMPLETED_PATH).exists(), "Completed human ratings"),
        ("Experiments", final_pack.HUMAN_EVAL_SUMMARY_PATH, not tables["human_eval_summary_table"].empty, "Aggregated human ratings"),
        ("Docs", DOCS_DIR / "final_report_draft.md", (DOCS_DIR / "final_report_draft.md").exists(), "Final report draft"),
        ("Docs", DOCS_DIR / "final_presentation_draft.md", (DOCS_DIR / "final_presentation_draft.md").exists(), "Presentation draft"),
        ("Docs", DOCS_DIR / "demo_script.md", (DOCS_DIR / "demo_script.md").exists(), "Demo script"),
        ("Docs", DOCS_DIR / "results_summary_draft.md", (DOCS_DIR / "results_summary_draft.md").exists(), "Results summary draft"),
        ("Docs", DOCS_DIR / "final_report_submission_checklist.md", (DOCS_DIR / "final_report_submission_checklist.md").exists(), "Submission checklist"),
    ]

    lines: list[str] = [
        "# Report Status",
        "",
        "This status report tracks the files that support the final course submission.",
        "",
        "## Summary",
    ]
    for point in summary["summary_points"]:
        lines.append(f"- {point}")

    lines.extend([
        "",
        "## File Availability",
        "| Category | File | Exists | Purpose |",
        "| --- | --- | --- | --- |",
    ])
    for category, path, exists, purpose in file_rows:
        lines.append(
            f"| {_cell_to_text(category)} | `{_display_path(path)}` | {'Yes' if exists else 'No'} | {_cell_to_text(purpose)} |"
        )

    manual_items: list[str] = []
    if Path(final_pack.HUMAN_RATING_SHEET_COMPLETED_PATH).exists():
        if tables["human_eval_summary_table"].empty:
            manual_items.append(
                "Run the aggregation step on the completed human ratings so the final averages appear in the report."
            )
    else:
        manual_items.append(
            "Collect completed human ratings in `experiments/human_rating_sheet_completed.csv`."
        )
        manual_items.append(
            "Aggregate the completed ratings to populate `experiments/human_eval_summary.csv` and the human-evaluation plots."
        )

    if tables["ablation_table"].empty:
        manual_items.append("Generate or restore the ablation study CSV before final submission.")
    if tables["alpha_table"].empty:
        manual_items.append("Generate or restore the alpha sensitivity CSV before final submission.")
    if tables["case_study_table"].empty:
        manual_items.append("Generate or restore the case-study CSV before final submission.")

    lines.extend([
        "",
        "## Complete Assets",
    ])
    complete_assets = [purpose for _, _, exists, purpose in file_rows if exists]
    for asset in complete_assets:
        lines.append(f"- {asset}")

    lines.extend([
        "",
        "## Still Needs Manual Completion",
    ])
    if manual_items:
        for item in manual_items:
            lines.append(f"- {item}")
    else:
        lines.append("- No blocking manual steps remain for the report package.")

    path = _ensure_parent(output_path)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return str(path)

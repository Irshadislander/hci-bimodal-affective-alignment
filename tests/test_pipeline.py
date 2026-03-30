"""Smoke tests for the Day 9 emotion pipeline."""

from __future__ import annotations

from math import isclose

import pandas as pd

from app.evaluation import evaluate_case
from app.case_studies import (
    DEFAULT_CASE_STUDIES,
    generate_case_study_table,
)
from app.final_evaluation_pack import (
    aggregate_human_ratings,
    build_human_rating_sheet,
    build_mode_comparison_cases,
    validate_completed_human_ratings,
)
from app.experiment_runner import (
    DEFAULT_CASES,
    run_ablation_study,
    run_alpha_sensitivity,
)
from app.face_emotion import detect_face_emotion_from_image, map_deepface_emotions
from app.fusion import fuse_emotions
from app.final_report_builder import (
    build_report_result_tables,
    export_report_status,
    export_report_tables_markdown,
    summarize_for_conclusion,
)
from app.human_eval import (
    HUMAN_EVAL_COLUMNS,
    make_human_eval_template,
    save_human_eval_template,
)
from app.plot_results import (
    plot_ablation_counts,
    plot_alpha_sensitivity,
    plot_case_type_distribution,
    plot_helpfulness_summary,
    plot_human_eval_summary,
)
from app.report_assets import summarize_results_for_report
from app.response_generator import generate_response
from app.text_emotion import (
    EMOTIONS,
    detect_text_emotion,
    detect_text_emotion_rule_based,
    map_model_outputs_to_project_emotions,
)


def _sample_probs(happy: float = 0.1, sad: float = 0.2, angry: float = 0.05, neutral: float = 0.55) -> dict[str, float]:
    """Build a simple normalized seven-emotion probability dictionary."""

    probs = {
        "happy": happy,
        "sad": sad,
        "angry": angry,
        "neutral": neutral,
        "fear": 0.04,
        "surprise": 0.03,
        "disgust": 0.03,
    }
    total = sum(probs.values())
    return {emotion: value / total for emotion, value in probs.items()}


def _table_columns(table) -> list[str]:
    """Return column names for either a pandas DataFrame or a row list."""

    if hasattr(table, "columns"):
        return list(table.columns)
    if table:
        return list(table[0].keys())
    return []


def _table_length(table) -> int:
    """Return row count for either a pandas DataFrame or a row list."""

    return len(table)


def _patch_final_evaluation_pack(monkeypatch, tmp_path) -> None:
    """Redirect final-evaluation outputs to a temporary directory."""

    monkeypatch.setattr(
        "app.final_evaluation_pack.detect_text_emotion",
        lambda text: _sample_probs(),
    )
    monkeypatch.setattr(
        "app.final_evaluation_pack.generate_response",
        lambda user_text, emotion: f"{emotion}: {user_text[:24]}",
    )
    monkeypatch.setattr(
        "app.final_evaluation_pack.MODE_COMPARISON_CASES_PATH",
        tmp_path / "mode_comparison_cases.csv",
    )
    monkeypatch.setattr(
        "app.final_evaluation_pack.HUMAN_RATING_SHEET_PATH",
        tmp_path / "human_rating_sheet.csv",
    )
    monkeypatch.setattr(
        "app.final_evaluation_pack.HUMAN_EVAL_SUMMARY_PATH",
        tmp_path / "human_eval_summary.csv",
    )


def _patch_report_builder_inputs(monkeypatch, tmp_path) -> None:
    """Create temporary report-builder inputs and point the modules at them."""

    ablation_df = pd.DataFrame(
        [
            {
                "case_id": 1,
                "user_text": "I am happy.",
                "alpha": 0.5,
                "text_top_emotion": "happy",
                "text_top_probability": 0.72,
                "face_top_emotion": "neutral",
                "face_top_probability": 0.61,
                "fused_top_emotion": "happy",
                "fused_top_probability": 0.66,
                "text_only_top_emotion": "happy",
                "face_only_top_emotion": "neutral",
                "empathetic_response": "That sounds uplifting.",
            },
            {
                "case_id": 2,
                "user_text": "I am sad.",
                "alpha": 0.5,
                "text_top_emotion": "sad",
                "text_top_probability": 0.70,
                "face_top_emotion": "sad",
                "face_top_probability": 0.64,
                "fused_top_emotion": "sad",
                "fused_top_probability": 0.68,
                "text_only_top_emotion": "sad",
                "face_only_top_emotion": "sad",
                "empathetic_response": "I am sorry you are dealing with that.",
            },
        ]
    )
    alpha_df = pd.DataFrame(
        [
            {
                "case_id": 1,
                "user_text": "I am happy.",
                "alpha": 0.0,
                "text_top_emotion": "happy",
                "text_top_probability": 0.72,
                "face_top_emotion": "neutral",
                "face_top_probability": 0.61,
                "fused_top_emotion": "neutral",
                "fused_top_probability": 0.61,
                "text_only_top_emotion": "happy",
                "face_only_top_emotion": "neutral",
                "empathetic_response": "That sounds uplifting.",
            },
            {
                "case_id": 1,
                "user_text": "I am happy.",
                "alpha": 1.0,
                "text_top_emotion": "happy",
                "text_top_probability": 0.72,
                "face_top_emotion": "neutral",
                "face_top_probability": 0.61,
                "fused_top_emotion": "happy",
                "fused_top_probability": 0.72,
                "text_only_top_emotion": "happy",
                "face_only_top_emotion": "neutral",
                "empathetic_response": "That sounds uplifting.",
            },
        ]
    )
    case_df = pd.DataFrame(
        [
            {
                "case_id": 1,
                "user_text": "I am happy.",
                "text_top_emotion": "happy",
                "face_top_emotion": "neutral",
                "fused_top_emotion": "happy",
                "empathetic_response": "That sounds uplifting.",
                "case_type": "Congruent",
            },
            {
                "case_id": 2,
                "user_text": "I am sad.",
                "text_top_emotion": "sad",
                "face_top_emotion": "sad",
                "fused_top_emotion": "sad",
                "empathetic_response": "I am sorry you are dealing with that.",
                "case_type": "Dissonant",
            },
            {
                "case_id": 3,
                "user_text": "I am okay.",
                "text_top_emotion": "neutral",
                "face_top_emotion": "neutral",
                "fused_top_emotion": "neutral",
                "empathetic_response": "Thanks for checking in.",
                "case_type": "Ambiguous",
            },
        ]
    )
    mode_df = pd.DataFrame(
        [
            {
                "case_id": 1,
                "user_text": "I am happy.",
                "text_top_emotion": "happy",
                "face_top_emotion": "neutral",
                "fused_top_emotion": "happy",
                "text_only_response": "That sounds uplifting.",
                "face_only_response": "I am here with you.",
                "fused_response": "That sounds uplifting.",
                "case_type": "Congruent",
            },
            {
                "case_id": 2,
                "user_text": "I am sad.",
                "text_top_emotion": "sad",
                "face_top_emotion": "sad",
                "fused_top_emotion": "sad",
                "text_only_response": "I am sorry you are dealing with that.",
                "face_only_response": "I am here with you.",
                "fused_response": "I am sorry you are dealing with that.",
                "case_type": "Dissonant",
            },
        ]
    )
    human_summary_df = pd.DataFrame(
        [
            {
                "mode": "text_only",
                "completed_rows": 6,
                "empathy_rating_mean": 3.0,
                "social_presence_rating_mean": 2.8,
                "trust_rating_mean": 3.1,
                "helpfulness_rating_mean": 3.2,
            },
            {
                "mode": "face_only",
                "completed_rows": 6,
                "empathy_rating_mean": 2.7,
                "social_presence_rating_mean": 2.6,
                "trust_rating_mean": 2.8,
                "helpfulness_rating_mean": 2.9,
            },
            {
                "mode": "fused",
                "completed_rows": 6,
                "empathy_rating_mean": 3.5,
                "social_presence_rating_mean": 3.4,
                "trust_rating_mean": 3.6,
                "helpfulness_rating_mean": 3.7,
            },
        ]
    )
    completed_rating_df = pd.DataFrame(
        [
            {
                "rater_id": "r1",
                "case_id": 1,
                "case_type": "Congruent",
                "user_text": "I am happy.",
                "mode": "fused",
                "detected_emotion": "happy",
                "system_response": "That sounds uplifting.",
                "empathy_rating": 5,
                "social_presence_rating": 4,
                "trust_rating": 4,
                "helpfulness_rating": 5,
                "notes": "Strong response.",
            }
        ]
    )

    ablation_path = tmp_path / "ablation_results.csv"
    alpha_path = tmp_path / "alpha_sensitivity.csv"
    case_path = tmp_path / "case_studies.csv"
    mode_path = tmp_path / "mode_comparison_cases.csv"
    summary_path = tmp_path / "human_eval_summary.csv"
    human_sheet_path = tmp_path / "human_rating_sheet.csv"
    completed_path = tmp_path / "human_rating_sheet_completed.csv"

    ablation_df.to_csv(ablation_path, index=False)
    alpha_df.to_csv(alpha_path, index=False)
    case_df.to_csv(case_path, index=False)
    mode_df.to_csv(mode_path, index=False)
    human_summary_df.to_csv(summary_path, index=False)
    completed_rating_df.to_csv(completed_path, index=False)
    pd.DataFrame(columns=[
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
    ]).to_csv(human_sheet_path, index=False)

    monkeypatch.setattr("app.report_assets.ABLATION_RESULTS_PATH", ablation_path)
    monkeypatch.setattr("app.report_assets.ALPHA_RESULTS_PATH", alpha_path)
    monkeypatch.setattr("app.report_assets.CASE_STUDIES_PATH", case_path)
    monkeypatch.setattr("app.final_evaluation_pack.MODE_COMPARISON_CASES_PATH", mode_path)
    monkeypatch.setattr("app.final_evaluation_pack.HUMAN_EVAL_SUMMARY_PATH", summary_path)
    monkeypatch.setattr("app.final_evaluation_pack.HUMAN_RATING_SHEET_PATH", human_sheet_path)
    monkeypatch.setattr("app.final_evaluation_pack.HUMAN_RATING_SHEET_COMPLETED_PATH", completed_path)


def test_text_detector_rule_based_returns_dict() -> None:
    """Rule-based text fallback should return a normalized probability dictionary."""

    text_probs = detect_text_emotion_rule_based("I am okay, but a little tired.")

    assert isinstance(text_probs, dict)
    assert set(text_probs) == set(EMOTIONS)
    assert isclose(sum(text_probs.values()), 1.0, abs_tol=1e-6)


def test_text_mapping_helper_returns_dict() -> None:
    """Transformer output mapping should return the project emotion schema."""

    raw_output = [
        {"label": "joy", "score": 0.72},
        {"label": "sadness", "score": 0.11},
        {"label": "anger", "score": 0.05},
        {"label": "neutral", "score": 0.08},
        {"label": "fear", "score": 0.02},
        {"label": "surprise", "score": 0.01},
        {"label": "disgust", "score": 0.01},
    ]
    probs = map_model_outputs_to_project_emotions(raw_output)

    assert isinstance(probs, dict)
    assert set(probs) == set(EMOTIONS)
    assert isclose(sum(probs.values()), 1.0, abs_tol=1e-6)


def test_detect_text_emotion_returns_dict(monkeypatch) -> None:
    """Overall text emotion detector should return a normalized probability dictionary."""

    class FakePipeline:
        def __call__(self, text, truncation=True):
            return [
                {"label": "joy", "score": 0.70},
                {"label": "sadness", "score": 0.10},
                {"label": "anger", "score": 0.05},
                {"label": "neutral", "score": 0.10},
                {"label": "fear", "score": 0.02},
                {"label": "surprise", "score": 0.02},
                {"label": "disgust", "score": 0.01},
            ]

    monkeypatch.setattr("app.text_emotion.load_text_emotion_pipeline", lambda: FakePipeline())

    probs = detect_text_emotion("I am excited and grateful.")

    assert isinstance(probs, dict)
    assert set(probs) == set(EMOTIONS)
    assert isclose(sum(probs.values()), 1.0, abs_tol=1e-6)
    assert probs["happy"] > probs["sad"]


def test_face_detector_returns_dict() -> None:
    """Face fallback path should return a normalized probability dictionary."""

    face_probs = detect_face_emotion_from_image(None)

    assert isinstance(face_probs, dict)
    assert set(face_probs) == set(EMOTIONS)
    assert isclose(sum(face_probs.values()), 1.0, abs_tol=1e-6)


def test_face_mapping_returns_dict() -> None:
    """DeepFace emotion mapping should return the project emotion schema."""

    raw_emotions = {
        "happy": 12.0,
        "sad": 8.0,
        "angry": 4.0,
        "neutral": 60.0,
        "fear": 5.0,
        "surprise": 6.0,
        "disgust": 5.0,
    }
    mapped = map_deepface_emotions(raw_emotions)

    assert isinstance(mapped, dict)
    assert set(mapped) == set(EMOTIONS)
    assert mapped["neutral"] == 60.0


def test_evaluation_case_returns_dict() -> None:
    """Case-level evaluation should return the expected summary keys."""

    case = evaluate_case(
        "I am okay, but a little tired.",
        _sample_probs(),
        {
            "happy": 0.08,
            "sad": 0.08,
            "angry": 0.05,
            "neutral": 0.62,
            "fear": 0.06,
            "surprise": 0.06,
            "disgust": 0.05,
        },
        0.5,
    )

    required_keys = {
        "user_text",
        "alpha",
        "text_top_emotion",
        "face_top_emotion",
        "fused_top_emotion",
        "text_only_top_emotion",
        "face_only_top_emotion",
        "empathetic_response",
    }
    assert isinstance(case, dict)
    assert required_keys <= set(case)
    assert case["fused_top_emotion"] in EMOTIONS
    assert isinstance(case["empathetic_response"], str)


def test_case_study_table_returns_dataframe(monkeypatch, tmp_path) -> None:
    """Case-study generation should return a table with the expected columns."""

    monkeypatch.setattr(
        "app.case_studies.detect_text_emotion",
        lambda text: _sample_probs(),
    )
    monkeypatch.setattr(
        "app.case_studies.CASE_STUDIES_OUTPUT_PATH",
        tmp_path / "case_studies.csv",
    )

    table = generate_case_study_table(alpha=0.5)

    expected_columns = {
        "case_id",
        "user_text",
        "text_top_emotion",
        "face_top_emotion",
        "fused_top_emotion",
        "empathetic_response",
        "case_type",
    }
    assert _table_length(table) == len(DEFAULT_CASE_STUDIES)
    assert expected_columns <= set(_table_columns(table))
    rows = table.to_dict(orient="records") if hasattr(table, "to_dict") else list(table)
    assert {row["case_type"] for row in rows} <= {"Congruent", "Dissonant", "Ambiguous"}
    assert (tmp_path / "case_studies.csv").exists()


def test_human_eval_template_returns_dataframe(monkeypatch, tmp_path) -> None:
    """Human evaluation templates should keep the expected rating columns."""

    monkeypatch.setattr(
        "app.case_studies.detect_text_emotion",
        lambda text: _sample_probs(),
    )
    monkeypatch.setattr(
        "app.case_studies.CASE_STUDIES_OUTPUT_PATH",
        tmp_path / "case_studies.csv",
    )

    case_table = generate_case_study_table(alpha=0.5)
    template = make_human_eval_template(case_table)
    saved_path = save_human_eval_template(template, str(tmp_path / "human_eval_template.csv"))

    assert _table_length(template) == len(DEFAULT_CASE_STUDIES)
    assert set(HUMAN_EVAL_COLUMNS) <= set(_table_columns(template))
    rows = template.to_dict(orient="records") if hasattr(template, "to_dict") else list(template)
    first_row = rows[0]
    assert first_row["empathy_rating"] == ""
    assert first_row["social_presence_rating"] == ""
    assert first_row["trust_rating"] == ""
    assert (tmp_path / "human_eval_template.csv").exists()
    assert saved_path.endswith("human_eval_template.csv")


def test_build_mode_comparison_cases_returns_dataframe(monkeypatch, tmp_path) -> None:
    """Mode comparison cases should return a table with text, face, and fused rows."""

    _patch_final_evaluation_pack(monkeypatch, tmp_path)

    df = build_mode_comparison_cases(alpha=0.5)

    expected_columns = {
        "case_id",
        "user_text",
        "text_top_emotion",
        "face_top_emotion",
        "fused_top_emotion",
        "text_only_response",
        "face_only_response",
        "fused_response",
        "case_type",
    }
    assert _table_length(df) == len(DEFAULT_CASE_STUDIES)
    assert expected_columns <= set(_table_columns(df))
    assert (tmp_path / "mode_comparison_cases.csv").exists()


def test_build_human_rating_sheet_returns_dataframe(monkeypatch, tmp_path) -> None:
    """Human rating sheets should return long-form comparison rows."""

    _patch_final_evaluation_pack(monkeypatch, tmp_path)

    df = build_human_rating_sheet(alpha=0.5)

    expected_columns = {
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
    }
    assert _table_length(df) == len(DEFAULT_CASE_STUDIES) * 3
    assert expected_columns <= set(_table_columns(df))
    rows = df.to_dict(orient="records") if hasattr(df, "to_dict") else list(df)
    first_row = rows[0]
    assert first_row["rater_id"] == ""
    assert first_row["empathy_rating"] == ""
    assert first_row["helpfulness_rating"] == ""
    assert (tmp_path / "human_rating_sheet.csv").exists()


def test_validate_completed_human_ratings_handles_missing_file(tmp_path) -> None:
    """Validation should return a safe report when the completed file is absent."""

    missing_path = tmp_path / "human_rating_sheet_completed.csv"

    report = validate_completed_human_ratings(str(missing_path))

    assert report["file_exists"] is False
    assert report["status"] == "missing_file"
    assert report["total_rows"] == 0
    assert report["completed_rows"] == 0
    assert set(report["missing_columns"]) == {
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
    }


def test_aggregate_human_ratings_handles_missing_file(monkeypatch, tmp_path) -> None:
    """Aggregation should return a blank summary when no completed file exists."""

    missing_path = tmp_path / "human_rating_sheet_completed.csv"
    monkeypatch.setattr(
        "app.final_evaluation_pack.HUMAN_EVAL_SUMMARY_PATH",
        tmp_path / "human_eval_summary.csv",
    )

    summary_dict, summary_df = aggregate_human_ratings(str(missing_path))

    assert summary_dict["status"] == "missing_file"
    assert summary_df.empty
    assert (tmp_path / "human_eval_summary.csv").exists()


def test_report_asset_summary_returns_dict(monkeypatch, tmp_path) -> None:
    """Report asset summary should return a dictionary of simple highlights."""

    ablation_df = pd.DataFrame(
        [
            {
                "case_id": 1,
                "user_text": "I am happy.",
                "alpha": 0.5,
                "fused_top_emotion": "happy",
            },
            {
                "case_id": 2,
                "user_text": "I am sad.",
                "alpha": 0.5,
                "fused_top_emotion": "sad",
            },
        ]
    )
    alpha_df = pd.DataFrame(
        [
            {"case_id": 1, "alpha": 0.0, "fused_top_emotion": "neutral"},
            {"case_id": 1, "alpha": 0.5, "fused_top_emotion": "happy"},
            {"case_id": 1, "alpha": 1.0, "fused_top_emotion": "happy"},
        ]
    )
    case_df = pd.DataFrame(
        [
            {"case_id": 1, "user_text": "A", "fused_top_emotion": "happy", "case_type": "Congruent"},
            {"case_id": 2, "user_text": "B", "fused_top_emotion": "sad", "case_type": "Dissonant"},
            {"case_id": 3, "user_text": "C", "fused_top_emotion": "neutral", "case_type": "Ambiguous"},
        ]
    )

    ablation_path = tmp_path / "ablation_results.csv"
    alpha_path = tmp_path / "alpha_sensitivity.csv"
    case_path = tmp_path / "case_studies.csv"
    ablation_df.to_csv(ablation_path, index=False)
    alpha_df.to_csv(alpha_path, index=False)
    case_df.to_csv(case_path, index=False)

    monkeypatch.setattr("app.report_assets.ABLATION_RESULTS_PATH", ablation_path)
    monkeypatch.setattr("app.report_assets.ALPHA_RESULTS_PATH", alpha_path)
    monkeypatch.setattr("app.report_assets.CASE_STUDIES_PATH", case_path)

    summary = summarize_results_for_report()

    assert isinstance(summary, dict)
    assert summary["number_of_cases"] == 3
    assert sorted(summary["unique_fused_emotions"]) == ["happy", "neutral", "sad"]
    assert summary["alpha_values_used"] == [0.0, 0.5, 1.0]
    assert summary["case_type_counts"] == {
        "Congruent": 1,
        "Dissonant": 1,
        "Ambiguous": 1,
    }


def test_plotting_functions_create_output_files(tmp_path) -> None:
    """Plot helpers should write PNG files for simple DataFrames."""

    ablation_df = pd.DataFrame(
        [
            {"fused_top_emotion": "happy"},
            {"fused_top_emotion": "sad"},
            {"fused_top_emotion": "happy"},
        ]
    )
    alpha_df = pd.DataFrame(
        [
            {"alpha": 0.0, "fused_top_emotion": "neutral"},
            {"alpha": 0.5, "fused_top_emotion": "happy"},
            {"alpha": 1.0, "fused_top_emotion": "happy"},
        ]
    )
    case_df = pd.DataFrame(
        [
            {"case_type": "Congruent"},
            {"case_type": "Dissonant"},
            {"case_type": "Ambiguous"},
        ]
    )

    ablation_path = plot_ablation_counts(ablation_df, output_path=tmp_path / "ablation_counts.png")
    alpha_path = plot_alpha_sensitivity(alpha_df, output_path=tmp_path / "alpha_sensitivity_plot.png")
    case_path = plot_case_type_distribution(case_df, output_path=tmp_path / "case_type_distribution.png")

    assert (tmp_path / "ablation_counts.png").exists()
    assert (tmp_path / "alpha_sensitivity_plot.png").exists()
    assert (tmp_path / "case_type_distribution.png").exists()
    assert ablation_path.endswith("ablation_counts.png")
    assert alpha_path.endswith("alpha_sensitivity_plot.png")
    assert case_path.endswith("case_type_distribution.png")


def test_human_eval_plotting_functions_create_output_files(tmp_path) -> None:
    """Human-evaluation plot helpers should write PNG files for simple summaries."""

    summary_df = pd.DataFrame(
        [
            {
                "mode": "text_only",
                "completed_rows": 6,
                "empathy_rating_mean": 3.0,
                "social_presence_rating_mean": 2.8,
                "trust_rating_mean": 3.1,
                "helpfulness_rating_mean": 3.2,
            },
            {
                "mode": "face_only",
                "completed_rows": 6,
                "empathy_rating_mean": 2.7,
                "social_presence_rating_mean": 2.6,
                "trust_rating_mean": 2.8,
                "helpfulness_rating_mean": 2.9,
            },
            {
                "mode": "fused",
                "completed_rows": 6,
                "empathy_rating_mean": 3.5,
                "social_presence_rating_mean": 3.4,
                "trust_rating_mean": 3.6,
                "helpfulness_rating_mean": 3.7,
            },
        ]
    )

    summary_path = plot_human_eval_summary(summary_df, output_path=tmp_path / "human_eval_summary_plot.png")
    helpfulness_path = plot_helpfulness_summary(summary_df, output_path=tmp_path / "helpfulness_summary_plot.png")

    assert (tmp_path / "human_eval_summary_plot.png").exists()
    assert (tmp_path / "helpfulness_summary_plot.png").exists()
    assert summary_path.endswith("human_eval_summary_plot.png")
    assert helpfulness_path.endswith("helpfulness_summary_plot.png")


def test_build_report_result_tables_returns_dict(monkeypatch, tmp_path) -> None:
    """Report builder should return the expected DataFrame dictionary."""

    _patch_report_builder_inputs(monkeypatch, tmp_path)

    tables = build_report_result_tables()

    expected_keys = {
        "ablation_table",
        "alpha_table",
        "case_study_table",
        "mode_comparison_table",
        "human_eval_summary_table",
    }
    assert expected_keys <= set(tables)
    assert all(isinstance(table, pd.DataFrame) for table in tables.values())
    assert not tables["human_eval_summary_table"].empty


def test_summarize_for_conclusion_returns_dict(monkeypatch, tmp_path) -> None:
    """Conclusion summary should describe the currently available result files."""

    _patch_report_builder_inputs(monkeypatch, tmp_path)

    summary = summarize_for_conclusion()

    assert isinstance(summary, dict)
    assert summary["number_of_experiment_cases"] == 2
    assert summary["supported_modes"] == ["text_only", "face_only", "fused"]
    assert summary["has_human_eval_summary"] is True
    assert summary["has_case_studies"] is True
    assert summary["has_alpha_sensitivity"] is True
    assert len(summary["summary_points"]) == 5


def test_export_report_tables_markdown_creates_file(monkeypatch, tmp_path) -> None:
    """Report tables markdown should be written to disk."""

    _patch_report_builder_inputs(monkeypatch, tmp_path)
    output_path = tmp_path / "report_tables.md"

    saved_path = export_report_tables_markdown(output_path=str(output_path))
    content = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert saved_path.endswith("report_tables.md")
    assert "# Report Tables" in content
    assert "## Ablation Table" in content
    assert "## Mode Comparison Table" in content


def test_export_report_status_creates_file(monkeypatch, tmp_path) -> None:
    """Report status markdown should be written to disk."""

    _patch_report_builder_inputs(monkeypatch, tmp_path)
    output_path = tmp_path / "report_status.md"

    saved_path = export_report_status(output_path=str(output_path))
    content = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert saved_path.endswith("report_status.md")
    assert "# Report Status" in content
    assert "## File Availability" in content
    assert "## Complete Assets" in content
    assert "No blocking manual steps remain" in content


def test_fusion_returns_dict_and_string() -> None:
    """Fusion should return a probability dictionary and top emotion label."""

    text_probs = detect_text_emotion_rule_based("I am okay, but a little tired.")
    face_probs = detect_face_emotion_from_image(None)
    fused_probs, fused_emotion = fuse_emotions(text_probs, face_probs, 0.5)

    assert isinstance(fused_probs, dict)
    assert isinstance(fused_emotion, str)
    assert set(fused_probs) == set(EMOTIONS)
    assert fused_emotion in EMOTIONS
    assert isclose(sum(fused_probs.values()), 1.0, abs_tol=1e-6)


def test_ablation_study_returns_dataframe(monkeypatch, tmp_path) -> None:
    """Ablation study should return and save a pandas DataFrame."""

    monkeypatch.setattr(
        "app.experiment_runner.detect_text_emotion",
        lambda text: _sample_probs(),
    )
    monkeypatch.setattr(
        "app.experiment_runner.ABLATION_RESULTS_PATH",
        tmp_path / "ablation_results.csv",
    )

    df = run_ablation_study(alpha=0.5)

    assert _table_length(df) == len(DEFAULT_CASES)
    assert {"case_id", "user_text", "alpha", "fused_top_emotion"} <= set(_table_columns(df))
    assert (tmp_path / "ablation_results.csv").exists()


def test_alpha_sensitivity_returns_dataframe(monkeypatch, tmp_path) -> None:
    """Alpha sensitivity should return and save a pandas DataFrame."""

    monkeypatch.setattr(
        "app.experiment_runner.detect_text_emotion",
        lambda text: _sample_probs(),
    )
    monkeypatch.setattr(
        "app.experiment_runner.ALPHA_SENSITIVITY_PATH",
        tmp_path / "alpha_sensitivity.csv",
    )

    df = run_alpha_sensitivity([0.0, 0.5, 1.0])

    assert _table_length(df) == len(DEFAULT_CASES) * 3
    assert {"case_id", "user_text", "alpha", "fused_top_emotion"} <= set(_table_columns(df))
    assert (tmp_path / "alpha_sensitivity.csv").exists()


def test_response_generator_returns_string() -> None:
    """Response generator should return a short non-empty string."""

    response = generate_response("I am okay, but a little tired.", "neutral")

    assert isinstance(response, str)
    assert response

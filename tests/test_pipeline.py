"""Smoke tests for the Day 5 emotion pipeline."""

from __future__ import annotations

from math import isclose

from app.evaluation import evaluate_case
from app.experiment_runner import (
    DEFAULT_CASES,
    run_ablation_study,
    run_alpha_sensitivity,
)
from app.face_emotion import detect_face_emotion_from_image, map_deepface_emotions
from app.fusion import fuse_emotions
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

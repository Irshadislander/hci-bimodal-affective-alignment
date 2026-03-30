"""Smoke tests for the Day 3 emotion pipeline."""

from __future__ import annotations

from math import isclose

from app.face_emotion import detect_face_emotion_from_image, map_deepface_emotions
from app.fusion import fuse_emotions
from app.response_generator import generate_response
from app.text_emotion import EMOTIONS, detect_text_emotion


def test_text_detector_returns_dict() -> None:
    """Text detector should return a normalized probability dictionary."""

    user_text = "I am okay, but a little tired."
    text_probs = detect_text_emotion(user_text)

    assert isinstance(text_probs, dict)
    assert set(text_probs) == set(EMOTIONS)
    assert isclose(sum(text_probs.values()), 1.0, abs_tol=1e-6)


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


def test_fusion_returns_dict_and_string() -> None:
    """Fusion should return a probability dictionary and top emotion label."""

    text_probs = detect_text_emotion("I am okay, but a little tired.")
    face_probs = detect_face_emotion_from_image(None)
    fused_probs, fused_emotion = fuse_emotions(text_probs, face_probs, 0.5)

    assert isinstance(fused_probs, dict)
    assert isinstance(fused_emotion, str)
    assert set(fused_probs) == set(EMOTIONS)
    assert fused_emotion in EMOTIONS
    assert isclose(sum(fused_probs.values()), 1.0, abs_tol=1e-6)


def test_response_generator_returns_string() -> None:
    """Response generator should return a short non-empty string."""

    response = generate_response("I am okay, but a little tired.", "neutral")

    assert isinstance(response, str)
    assert response

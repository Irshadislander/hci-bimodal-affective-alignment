"""Smoke test for the Day 1 emotion pipeline."""

from __future__ import annotations

from math import isclose

from app.face_emotion import detect_face_emotion
from app.fusion import fuse_emotions
from app.main import analyze
from app.response_generator import generate_response
from app.text_emotion import EMOTIONS, detect_text_emotion
from app.utils import pretty_probs


def test_pipeline_smoke() -> None:
    """Import the modules and run the main pipeline functions."""

    user_text = "I am okay, but a little tired."
    text_probs = detect_text_emotion(user_text)
    face_probs = detect_face_emotion()
    fused_probs, fused_emotion = fuse_emotions(text_probs, face_probs, 0.5)
    response = generate_response(user_text, fused_emotion)
    analysis = analyze(user_text, 0.5)

    for probs in (text_probs, face_probs, fused_probs):
        assert set(probs) == set(EMOTIONS)
        assert isclose(sum(probs.values()), 1.0, abs_tol=1e-6)

    assert fused_emotion in EMOTIONS
    assert isinstance(response, str) and response
    assert analysis["fused_emotion"] == fused_emotion
    assert analysis["response"] == response
    assert pretty_probs({"happy": 0.12345})["happy"] == 0.123

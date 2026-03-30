"""Case-level evaluation helpers for the Day 7 prototype."""

from __future__ import annotations

try:
    from app.fusion import fuse_emotions, get_top_n_emotions
    from app.response_generator import generate_response
except ImportError:  # pragma: no cover - supports running from app/ directly
    from fusion import fuse_emotions, get_top_n_emotions
    from response_generator import generate_response


def _top_emotion_summary(probs: dict[str, float]) -> tuple[str, float]:
    """Return the top emotion label and its probability."""

    top = get_top_n_emotions(probs, n=1)
    if not top:
        return "neutral", 0.0
    return top[0]


def run_text_only_case(text_probs: dict[str, float]) -> tuple[dict[str, float], str]:
    """Summarize the text-only modality."""

    top_emotion, _ = _top_emotion_summary(text_probs)
    return dict(text_probs), top_emotion


def run_face_only_case(face_probs: dict[str, float]) -> tuple[dict[str, float], str]:
    """Summarize the face-only modality."""

    top_emotion, _ = _top_emotion_summary(face_probs)
    return dict(face_probs), top_emotion


def run_fused_case(
    text_probs: dict[str, float],
    face_probs: dict[str, float],
    alpha: float,
) -> tuple[dict[str, float], str]:
    """Fuse text and face probabilities and return the top emotion."""

    fused_probs, top_emotion = fuse_emotions(text_probs, face_probs, alpha)
    return fused_probs, top_emotion


def evaluate_case(
    user_text: str,
    text_probs: dict[str, float],
    face_probs: dict[str, float],
    alpha: float,
) -> dict[str, object]:
    """Evaluate one case across text-only, face-only, and fused modes."""

    text_only_probs, text_only_top_emotion = run_text_only_case(text_probs)
    face_only_probs, face_only_top_emotion = run_face_only_case(face_probs)
    fused_probs, fused_top_emotion = run_fused_case(text_probs, face_probs, alpha)

    text_top_emotion, text_top_probability = _top_emotion_summary(text_probs)
    face_top_emotion, face_top_probability = _top_emotion_summary(face_probs)
    _, fused_top_probability = _top_emotion_summary(fused_probs)
    empathetic_response = generate_response(user_text, fused_top_emotion)

    return {
        "user_text": user_text,
        "alpha": float(alpha),
        "text_top_emotion": text_top_emotion,
        "text_top_probability": text_top_probability,
        "face_top_emotion": face_top_emotion,
        "face_top_probability": face_top_probability,
        "fused_top_emotion": fused_top_emotion,
        "fused_top_probability": fused_top_probability,
        "text_only_top_emotion": text_only_top_emotion,
        "face_only_top_emotion": face_only_top_emotion,
        "text_probs": dict(text_probs),
        "face_probs": dict(face_probs),
        "fused_probs": fused_probs,
        "text_only_probs": text_only_probs,
        "face_only_probs": face_only_probs,
        "empathetic_response": empathetic_response,
    }

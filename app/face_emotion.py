"""Image-based facial emotion analysis for the project."""

from __future__ import annotations

from io import BytesIO
from typing import Any

try:
    from app.text_emotion import EMOTIONS
    from app.utils import normalize_probs
except ImportError:  # pragma: no cover - supports running from app/ directly
    from text_emotion import EMOTIONS
    from utils import normalize_probs


_LAST_WARNING = ""

_FALLBACK_FACE_PROBS = {
    "happy": 0.08,
    "sad": 0.08,
    "angry": 0.05,
    "neutral": 0.62,
    "fear": 0.06,
    "surprise": 0.06,
    "disgust": 0.05,
}

_DEEPFACE_KEYS = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "neutral": "neutral",
    "fear": "fear",
    "surprise": "surprise",
    "disgust": "disgust",
}


def _set_warning(message: str) -> None:
    """Store the last analysis warning for the UI to consume."""

    global _LAST_WARNING
    _LAST_WARNING = message


def get_face_analysis_warning() -> str:
    """Return the warning message from the most recent face analysis."""

    return _LAST_WARNING


def _fallback_face_probs() -> dict[str, float]:
    """Return the safe fallback facial distribution."""

    return dict(_FALLBACK_FACE_PROBS)


def map_deepface_emotions(raw_emotions: dict) -> dict[str, float]:
    """Map DeepFace emotion keys into the project emotion schema."""

    if not isinstance(raw_emotions, dict):
        return {emotion: 0.0 for emotion in EMOTIONS}

    mapped = {}
    for emotion in EMOTIONS:
        key = _DEEPFACE_KEYS.get(emotion, emotion)
        mapped[emotion] = float(raw_emotions.get(key, raw_emotions.get(emotion, 0.0)))
    return mapped


def normalize_face_probs(probs: dict) -> dict[str, float]:
    """Normalize facial emotion scores and preserve a neutral fallback."""

    aligned = {emotion: max(0.0, float(probs.get(emotion, 0.0))) for emotion in EMOTIONS}
    if sum(aligned.values()) <= 0:
        return _fallback_face_probs()
    return normalize_probs(aligned)


def _to_rgb_array(image: Any):
    """Convert supported image inputs to an RGB numpy array."""

    try:
        import numpy as np
        from PIL import Image
    except Exception as exc:  # pragma: no cover - dependency guard
        raise RuntimeError("Image dependencies are unavailable.") from exc

    if hasattr(image, "getvalue"):
        image = image.getvalue()

    if isinstance(image, np.ndarray):
        return image
    if isinstance(image, (bytes, bytearray)):
        return np.asarray(Image.open(BytesIO(image)).convert("RGB"))
    if isinstance(image, str):
        return np.asarray(Image.open(image).convert("RGB"))
    if hasattr(image, "read"):
        return np.asarray(Image.open(image).convert("RGB"))
    if hasattr(image, "convert"):
        return np.asarray(image.convert("RGB"))

    raise TypeError("Unsupported image input type for facial analysis.")


def detect_face_emotion_from_image(image) -> dict[str, float]:
    """Analyze an uploaded image and return facial emotion probabilities."""

    if image is None:
        _set_warning("No image uploaded. Using a mostly neutral fallback facial distribution.")
        return _fallback_face_probs()

    try:
        image_array = _to_rgb_array(image)
        try:
            from deepface import DeepFace
        except Exception:
            _set_warning(
                "DeepFace is unavailable in this environment. "
                "Using a mostly neutral fallback facial distribution."
            )
            return _fallback_face_probs()

        result = DeepFace.analyze(
            img_path=image_array,
            actions=["emotion"],
            enforce_detection=False,
            silent=True,
        )
        if isinstance(result, list):
            result = result[0] if result and isinstance(result[0], dict) else {}

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected DeepFace result format.")

        raw_emotions = result.get("emotion") if isinstance(result.get("emotion"), dict) else result
        mapped = map_deepface_emotions(raw_emotions)
        _set_warning("")
        return normalize_face_probs(mapped)
    except Exception:
        _set_warning(
            "Facial analysis could not be completed. "
            "Using a mostly neutral fallback facial distribution."
        )
        return _fallback_face_probs()

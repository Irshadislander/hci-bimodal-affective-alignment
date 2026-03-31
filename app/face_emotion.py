"""DeepFace-first facial emotion runtime with safe image-based fallback."""

from __future__ import annotations

from io import BytesIO
from typing import Any

try:
    from app.text_emotion import EMOTIONS
    from app.utils import normalize_probs
except ImportError:  # pragma: no cover - supports running from app/ directly
    from text_emotion import EMOTIONS
    from utils import normalize_probs


_FACE_MODEL_NAME = "DeepFace Emotion"
_FACE_HEURISTIC_MODEL_NAME = "Image heuristic backup"

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

_FACE_LABEL_TO_PROJECT = {
    "happy": "happy",
    "happiness": "happy",
    "joy": "happy",
    "joyful": "happy",
    "smile": "happy",
    "positive": "happy",
    "sad": "sad",
    "sadness": "sad",
    "unhappy": "sad",
    "disappointed": "sad",
    "disappointment": "sad",
    "grief": "sad",
    "angry": "angry",
    "anger": "angry",
    "mad": "angry",
    "frustrated": "angry",
    "annoyed": "angry",
    "irritated": "angry",
    "neutral": "neutral",
    "calm": "neutral",
    "confused": "neutral",
    "bored": "neutral",
    "fear": "fear",
    "fearful": "fear",
    "anxious": "fear",
    "anxiety": "fear",
    "worried": "fear",
    "nervous": "fear",
    "surprise": "surprise",
    "surprised": "surprise",
    "astonished": "surprise",
    "amazed": "surprise",
    "disgust": "disgust",
    "disgusted": "disgust",
    "repulsed": "disgust",
    "gross": "disgust",
    "negative": "sad",
}

_FACE_ANALYZER: Any | None = None
_FACE_MODEL_CACHE: Any | None = None
_FACE_RUNTIME_INITIALIZED = False


def _make_face_runtime_status(
    *,
    runtime_mode: str,
    fallback_used: bool,
    face_runtime_active: bool,
    message: str,
    model_name: str | None = None,
    load_error: str | None = None,
    inference_error: str | None = None,
) -> dict[str, Any]:
    """Build a compact runtime-status dictionary for UI consumption."""

    status: dict[str, Any] = {
        "runtime_mode": runtime_mode,
        "model_name": model_name,
        "fallback_used": bool(fallback_used),
        "face_runtime_active": bool(face_runtime_active),
        "message": message,
    }
    if load_error:
        status["load_error"] = load_error
    if inference_error:
        status["inference_error"] = inference_error
    return status


_FACE_RUNTIME_STATUS = _make_face_runtime_status(
    runtime_mode="fallback_rule_based",
    fallback_used=True,
    face_runtime_active=False,
    message=(
        "Face runtime has not been initialized yet. "
        "The image-based analyzer will activate on first use."
    ),
)


def _short_error_message(exc: BaseException, limit: int = 220) -> str:
    """Return a short, readable error message for runtime status records."""

    message = f"{exc.__class__.__name__}: {exc}"
    if len(message) <= limit:
        return message
    return f"{message[: limit - 3].rstrip()}..."


def _set_warning(message: str) -> None:
    """Store the last analysis warning for the UI to consume."""

    global _LAST_WARNING
    _LAST_WARNING = message


def get_face_analysis_warning() -> str:
    """Return the warning message from the most recent face analysis."""

    return _LAST_WARNING


def _store_face_runtime_status(status: dict[str, Any]) -> dict[str, Any]:
    """Persist the runtime status and return a defensive copy."""

    global _FACE_RUNTIME_STATUS
    _FACE_RUNTIME_STATUS = dict(status)
    return dict(_FACE_RUNTIME_STATUS)


def _merge_face_runtime_status(**updates: Any) -> dict[str, Any]:
    """Update the runtime status while preserving fields that were not changed."""

    status = dict(_FACE_RUNTIME_STATUS)
    for key, value in updates.items():
        if value is None:
            status.pop(key, None)
        else:
            status[key] = value
    return _store_face_runtime_status(status)


def get_face_runtime_status() -> dict[str, Any]:
    """Return the current face runtime status."""

    return dict(_FACE_RUNTIME_STATUS)


def get_face_fallback_distribution() -> dict[str, float]:
    """Return the safe neutral-leaning fallback facial distribution."""

    return dict(_FALLBACK_FACE_PROBS)


def _fallback_face_probs() -> dict[str, float]:
    """Return the safe fallback facial distribution."""

    return get_face_fallback_distribution()


def _normalize_face_label(label: str) -> str | None:
    """Map a raw label into one of the project emotions when possible."""

    normalized = str(label).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in EMOTIONS:
        return normalized
    return _FACE_LABEL_TO_PROJECT.get(normalized)


def _coerce_face_scores(raw_output: Any) -> dict[str, float]:
    """Coerce DeepFace-style or heuristic outputs into aligned project scores."""

    aligned = {emotion: 0.0 for emotion in EMOTIONS}

    if isinstance(raw_output, list):
        if len(raw_output) == 1 and isinstance(raw_output[0], dict):
            return _coerce_face_scores(raw_output[0])

        any_scores = False
        for item in raw_output:
            if not isinstance(item, dict):
                continue
            if "label" in item and "score" in item:
                project_emotion = _normalize_face_label(item["label"])
                if project_emotion is not None:
                    aligned[project_emotion] += float(item.get("score", 0.0))
                    any_scores = True
                continue
            for key, value in item.items():
                project_emotion = _normalize_face_label(key)
                if project_emotion is not None:
                    aligned[project_emotion] += float(value)
                    any_scores = True
        return aligned if any_scores else {emotion: 0.0 for emotion in EMOTIONS}

    if isinstance(raw_output, dict):
        nested = raw_output.get("emotion")
        if isinstance(nested, dict):
            return _coerce_face_scores(nested)

        nested = raw_output.get("scores")
        if isinstance(nested, dict):
            return _coerce_face_scores(nested)

        any_scores = False
        for key, value in raw_output.items():
            project_emotion = _normalize_face_label(key)
            if project_emotion is not None:
                aligned[project_emotion] += float(value)
                any_scores = True
        return aligned if any_scores else {emotion: 0.0 for emotion in EMOTIONS}

    return {emotion: 0.0 for emotion in EMOTIONS}


def map_face_outputs_to_project_emotions(raw_output: Any) -> dict[str, float]:
    """Map face-emotion outputs into the project's seven-class schema."""

    return normalize_face_probs(_coerce_face_scores(raw_output))


def map_deepface_emotions(raw_emotions: Any) -> dict[str, float]:
    """Compatibility alias for older imports and tests."""

    return map_face_outputs_to_project_emotions(raw_emotions)


def normalize_face_probs(probs: dict[str, float]) -> dict[str, float]:
    """Normalize facial emotion scores and preserve a safe fallback."""

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


def _center_crop(image_array: Any):
    """Return a stable center crop when face detection is unavailable."""

    try:
        import numpy as np
    except Exception as exc:  # pragma: no cover - dependency guard
        raise RuntimeError("Image dependencies are unavailable.") from exc

    array = np.asarray(image_array)
    if array.ndim < 2 or min(array.shape[:2]) < 4:
        return array

    height, width = array.shape[:2]
    crop_h = max(1, int(height * 0.8))
    crop_w = max(1, int(width * 0.8))
    top = max(0, (height - crop_h) // 2)
    left = max(0, (width - crop_w) // 2)
    return array[top : top + crop_h, left : left + crop_w]


def _extract_face_roi(image_array: Any):
    """Attempt to detect and crop the most prominent face region."""

    try:
        import cv2
    except Exception:
        return _center_crop(image_array)

    try:
        array = (
            cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            if getattr(image_array, "ndim", 0) == 3
            else image_array
        )
        cascade_dir = getattr(getattr(cv2, "data", None), "haarcascades", "")
        if not cascade_dir:
            return _center_crop(image_array)

        detector = cv2.CascadeClassifier(cascade_dir + "haarcascade_frontalface_default.xml")
        faces = detector.detectMultiScale(array, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))
        if faces is None or len(faces) == 0:
            return _center_crop(image_array)

        x, y, w, h = max(faces, key=lambda rect: int(rect[2]) * int(rect[3]))
        pad_x = max(4, int(w * 0.15))
        pad_y = max(4, int(h * 0.15))

        height, width = image_array.shape[:2]
        x0 = max(0, int(x) - pad_x)
        y0 = max(0, int(y) - pad_y)
        x1 = min(width, int(x + w) + pad_x)
        y1 = min(height, int(y + h) + pad_y)
        return image_array[y0:y1, x0:x1]
    except Exception:
        return _center_crop(image_array)


def _heuristic_face_scores(image_array: Any) -> dict[str, float]:
    """Generate a stable backup face-emotion score distribution from an image."""

    try:
        import numpy as np
    except Exception as exc:  # pragma: no cover - dependency guard
        raise RuntimeError("Image dependencies are unavailable.") from exc

    roi = _extract_face_roi(image_array)
    rgb = np.asarray(roi, dtype=np.float32)
    if rgb.ndim == 2:
        rgb = np.stack([rgb, rgb, rgb], axis=-1)
    if rgb.ndim != 3 or rgb.shape[2] < 3:
        raise RuntimeError("Uploaded image could not be converted for analysis.")
    if rgb.shape[2] > 3:
        rgb = rgb[:, :, :3]
    if rgb.size == 0:
        raise RuntimeError("Uploaded image could not be analyzed.")

    if float(rgb.max()) > 1.0:
        rgb = rgb / 255.0

    brightness = float(rgb.mean())
    contrast = float(rgb.std())
    channel_means = rgb.mean(axis=(0, 1))
    red = float(channel_means[0])
    green = float(channel_means[1])
    blue = float(channel_means[2])
    saturation = float((rgb.max(axis=2) - rgb.min(axis=2)).mean())
    warmth = max(0.0, red - blue)
    coolness = max(0.0, blue - red)
    green_bias = max(0.0, green - (red + blue) / 2.0)
    centered_brightness = 1.0 - min(1.0, abs(brightness - 0.55) / 0.55)
    calmness = 1.0 - min(1.0, (contrast + saturation * 0.5))

    scores = {
        "happy": 0.15 + 1.8 * brightness + 1.0 * saturation + 0.4 * warmth,
        "sad": 0.15 + 1.7 * max(0.0, 0.5 - brightness) + 0.7 * (1.0 - saturation) + 0.4 * coolness,
        "angry": 0.15 + 1.2 * contrast + 0.7 * warmth + 0.5 * saturation,
        "neutral": 0.22 + 1.3 * centered_brightness + 0.8 * calmness,
        "fear": 0.14 + 1.1 * max(0.0, 0.55 - brightness) + 0.9 * contrast + 0.3 * coolness,
        "surprise": 0.14 + 1.4 * contrast + 0.8 * brightness + 0.4 * saturation,
        "disgust": 0.12 + 0.9 * green_bias + 0.6 * max(0.0, 0.5 - brightness) + 0.4 * (1.0 - saturation),
    }
    return {emotion: max(0.0, float(score)) for emotion, score in scores.items()}


def _attempt_face_runtime_initialization() -> tuple[Any | None, dict[str, Any]]:
    """Attempt to initialize the DeepFace runtime and its cached model."""

    global _FACE_MODEL_CACHE

    try:
        from deepface import DeepFace
    except Exception as exc:
        load_error = _short_error_message(exc)
        status = _make_face_runtime_status(
            runtime_mode="image_heuristic",
            model_name=_FACE_HEURISTIC_MODEL_NAME,
            fallback_used=True,
            face_runtime_active=True,
            message=(
                "DeepFace could not be imported. "
                "Using the image-based heuristic backup runtime."
            ),
            load_error=load_error,
        )
        return None, status

    build_model = getattr(DeepFace, "build_model", None)
    if callable(build_model):
        build_errors: list[str] = []
        candidate_calls = [
            ((), {"model_name": "Emotion"}),
            (("Emotion",), {}),
            ((), {"model_name": "emotion"}),
            (("emotion",), {}),
        ]
        for args, kwargs in candidate_calls:
            try:
                model = build_model(*args, **kwargs)
                _FACE_MODEL_CACHE = model
                status = _make_face_runtime_status(
                    runtime_mode="deepface",
                    model_name=_FACE_MODEL_NAME,
                    fallback_used=False,
                    face_runtime_active=True,
                    message=(
                        "DeepFace emotion model loaded successfully and cached "
                        "for image inference."
                    ),
                )
                return DeepFace, status
            except Exception as exc:
                build_errors.append(_short_error_message(exc))

        load_error = build_errors[-1] if build_errors else "DeepFace emotion model could not be built."
        status = _make_face_runtime_status(
            runtime_mode="image_heuristic",
            model_name=_FACE_HEURISTIC_MODEL_NAME,
            fallback_used=True,
            face_runtime_active=True,
            message=(
                "DeepFace was available, but the emotion model could not be built. "
                "Using the image-based heuristic backup runtime."
            ),
            load_error=load_error,
        )
        return None, status

    status = _make_face_runtime_status(
        runtime_mode="deepface",
        model_name=_FACE_MODEL_NAME,
        fallback_used=False,
        face_runtime_active=True,
        message="DeepFace imported successfully and is ready for face inference.",
    )
    return DeepFace, status


def initialize_face_runtime() -> dict[str, Any]:
    """Explicitly initialize and cache the face-analysis runtime."""

    global _FACE_ANALYZER, _FACE_RUNTIME_INITIALIZED

    if _FACE_RUNTIME_INITIALIZED:
        return get_face_runtime_status()

    analyzer, status = _attempt_face_runtime_initialization()
    _FACE_ANALYZER = analyzer
    _FACE_RUNTIME_INITIALIZED = True
    _set_warning("")
    return _store_face_runtime_status(status)


def _run_face_inference(image_array: Any) -> Any:
    """Run inference using the active runtime backend."""

    runtime_status = get_face_runtime_status()
    runtime_mode = str(runtime_status.get("runtime_mode", "fallback_rule_based"))

    if runtime_mode == "deepface":
        if _FACE_ANALYZER is None:
            raise RuntimeError("DeepFace runtime is not initialized.")
        return _FACE_ANALYZER.analyze(
            img_path=image_array,
            actions=["emotion"],
            enforce_detection=False,
            silent=True,
        )
    if runtime_mode == "image_heuristic":
        return _heuristic_face_scores(image_array)

    raise RuntimeError("Face runtime is not initialized.")


def detect_face_emotion_from_image(image) -> dict[str, float]:
    """Analyze an uploaded image and return facial emotion probabilities."""

    initialize_face_runtime()

    if image is None:
        message = "No image uploaded. Using the safe fallback facial distribution."
        _set_warning(message)
        _merge_face_runtime_status(
            fallback_used=True,
            message=message,
            inference_error=None,
        )
        return _fallback_face_probs()

    try:
        image_array = _to_rgb_array(image)
        result = _run_face_inference(image_array)
        mapped = map_face_outputs_to_project_emotions(result)

        if sum(mapped.values()) <= 0:
            raise RuntimeError("Face analyzer returned an empty emotion distribution.")

        runtime_mode = str(get_face_runtime_status().get("runtime_mode", "fallback_rule_based"))
        if runtime_mode == "deepface":
            message = "DeepFace inferred facial emotion probabilities from the uploaded image."
            fallback_used = False
        else:
            message = (
                "DeepFace was unavailable, so the image-based heuristic backup "
                "analyzed the uploaded image."
            )
            fallback_used = True

        _merge_face_runtime_status(
            fallback_used=fallback_used,
            message=message,
            inference_error=None,
        )
        _set_warning("" if not fallback_used else message)
        return normalize_face_probs(mapped)
    except Exception as exc:
        error_message = _short_error_message(exc)
        fallback_message = (
            "Facial analysis could not be completed. "
            "Using the safe fallback facial distribution."
        )
        _merge_face_runtime_status(
            fallback_used=True,
            message=fallback_message,
            inference_error=error_message,
        )
        _set_warning(fallback_message)
        return _fallback_face_probs()

"""Streamlit demo app for the bimodal affective alignment starter."""

from __future__ import annotations

try:
    from app.face_emotion import detect_face_emotion
    from app.fusion import fuse_emotions
    from app.response_generator import generate_response
    from app.text_emotion import detect_text_emotion
    from app.utils import pretty_probs
except ImportError:  # pragma: no cover - supports running from app/ directly
    from face_emotion import detect_face_emotion
    from fusion import fuse_emotions
    from response_generator import generate_response
    from text_emotion import detect_text_emotion
    from utils import pretty_probs


DEFAULT_TEXT = "I am okay, but a little tired."


def analyze(user_text: str, alpha: float) -> dict[str, object]:
    """Run the full emotion pipeline for the demo."""

    text_probs = detect_text_emotion(user_text)
    face_probs = detect_face_emotion()
    fused_probs, fused_emotion = fuse_emotions(text_probs, face_probs, alpha)
    response = generate_response(user_text, fused_emotion)
    return {
        "text_probs": text_probs,
        "face_probs": face_probs,
        "fused_probs": fused_probs,
        "fused_emotion": fused_emotion,
        "response": response,
    }


def main() -> None:
    """Render the Streamlit user interface."""

    import streamlit as st

    st.set_page_config(
        page_title="HCI Bimodal Affective Alignment",
        layout="centered",
    )

    st.title("HCI Bimodal Affective Alignment")
    st.write(
        "A Day 1 research-style demo that combines rule-based text emotion "
        "recognition, mock facial emotion recognition, weighted fusion, and "
        "empathetic response generation."
    )

    user_text = st.text_input(
        "Text input",
        value=DEFAULT_TEXT,
        help="Enter a short message to analyze.",
    )
    alpha = st.slider(
        "Text weight (alpha)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
    )

    if st.button("Run Analysis"):
        results = analyze(user_text, alpha)

        st.subheader("Emotion Probabilities")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("Text")
            st.json(pretty_probs(results["text_probs"]))
        with col2:
            st.caption("Face")
            st.json(pretty_probs(results["face_probs"]))
        with col3:
            st.caption("Fused")
            st.json(pretty_probs(results["fused_probs"]))

        st.subheader("Final Output")
        st.metric("Fused emotion", results["fused_emotion"])
        st.info(results["response"])


if __name__ == "__main__":
    main()

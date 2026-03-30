"""Streamlit demo app for the bimodal affective alignment prototype."""

from __future__ import annotations

try:
    from app.face_emotion import detect_face_emotion
    from app.fusion import get_top_n_emotions, fuse_emotions
    from app.response_generator import generate_response
    from app.text_emotion import detect_text_emotion
    from app.utils import pretty_probs, probs_to_dataframe
except ImportError:  # pragma: no cover - supports running from app/ directly
    from face_emotion import detect_face_emotion
    from fusion import get_top_n_emotions, fuse_emotions
    from response_generator import generate_response
    from text_emotion import detect_text_emotion
    from utils import pretty_probs, probs_to_dataframe

import pandas as pd

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


def _emotion_callout(st, emotion: str, label: str) -> None:
    """Render a short status callout based on the detected emotion."""

    message = f"{label}: {emotion.title()}"
    if emotion == "happy":
        st.success(message)
    elif emotion == "neutral":
        st.info(message)
    else:
        st.warning(message)


def _probability_table(probs: dict[str, float]) -> pd.DataFrame:
    """Build a display-ready probability table."""

    return probs_to_dataframe(pretty_probs(probs))


def main() -> None:
    """Render the Streamlit user interface."""

    import streamlit as st

    st.set_page_config(
        page_title="HCI Bimodal Affective Alignment",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("HCI Bimodal Affective Alignment")
    st.write(
        "A mini research-style prototype that combines text emotion recognition, "
        "simulated facial emotion recognition, weighted fusion, and empathetic "
        "response generation."
    )

    with st.sidebar:
        st.header("Project Summary")
        st.write(
            "This prototype studies bimodal affective alignment by combining text "
            "and facial cues before generating a short supportive response."
        )
        st.write("Current stage: Day 2 Prototype")
        st.caption(
            "Facial emotion is simulated for prototype evaluation and ablation work."
        )

    with st.form("analysis_form"):
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
        submitted = st.form_submit_button("Run Analysis")

    if submitted:
        results = analyze(user_text, alpha)
        text_top = get_top_n_emotions(results["text_probs"], n=1)[0][0]
        face_top = get_top_n_emotions(results["face_probs"], n=1)[0][0]
        fused_top_3 = get_top_n_emotions(results["fused_probs"], n=3)

        st.markdown("### A) Text Emotion")
        st.dataframe(_probability_table(results["text_probs"]), use_container_width=True)
        _emotion_callout(st, text_top, "Text signal")

        st.markdown("### B) Face Emotion")
        st.dataframe(_probability_table(results["face_probs"]), use_container_width=True)
        st.warning("Facial emotion is currently simulated for prototype evaluation.")
        _emotion_callout(st, face_top, "Face signal")

        st.markdown("### C) Fused Emotion")
        st.dataframe(_probability_table(results["fused_probs"]), use_container_width=True)
        top_3_frame = pd.DataFrame(
            [
                {
                    "Rank": rank,
                    "Emotion": emotion.title(),
                    "Probability": round(probability, 3),
                }
                for rank, (emotion, probability) in enumerate(fused_top_3, start=1)
            ]
        ).set_index("Rank")
        st.caption("Top 3 emotions from the fused distribution")
        st.dataframe(top_3_frame, use_container_width=True)

        st.markdown("### D) Final Detected Emotion")
        final_emotion = results["fused_emotion"]
        _emotion_callout(st, final_emotion, "Final detected emotion")
        st.metric("Detected emotion", final_emotion.title())

        st.markdown("### E) Empathetic Response")
        st.info(results["response"])


if __name__ == "__main__":
    main()

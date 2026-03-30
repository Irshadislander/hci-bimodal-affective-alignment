"""Streamlit demo app for the bimodal affective alignment prototype."""

from __future__ import annotations

try:
    from app.face_emotion import (
        detect_face_emotion_from_image,
        get_face_analysis_warning,
    )
    from app.experiment_runner import (
        ABLATION_RESULTS_PATH,
        ALPHA_SENSITIVITY_PATH,
        DEFAULT_ALPHA_GRID,
        run_ablation_study,
        run_alpha_sensitivity,
    )
    from app.case_studies import (
        CASE_STUDIES_OUTPUT_PATH,
        generate_case_study_table,
    )
    from app.human_eval import (
        HUMAN_EVAL_TEMPLATE_PATH,
        make_human_eval_template,
        save_human_eval_template,
    )
    from app.fusion import get_top_n_emotions, fuse_emotions
    from app.response_generator import generate_response
    from app.text_emotion import (
        detect_text_emotion,
        get_text_emotion_backend_status,
    )
    from app.utils import probs_to_dataframe
except ImportError:  # pragma: no cover - supports running from app/ directly
    from face_emotion import detect_face_emotion_from_image, get_face_analysis_warning
    from experiment_runner import (
        ABLATION_RESULTS_PATH,
        ALPHA_SENSITIVITY_PATH,
        DEFAULT_ALPHA_GRID,
        run_ablation_study,
        run_alpha_sensitivity,
    )
    from case_studies import CASE_STUDIES_OUTPUT_PATH, generate_case_study_table
    from human_eval import (
        HUMAN_EVAL_TEMPLATE_PATH,
        make_human_eval_template,
        save_human_eval_template,
    )
    from fusion import get_top_n_emotions, fuse_emotions
    from response_generator import generate_response
    from text_emotion import detect_text_emotion, get_text_emotion_backend_status
    from utils import probs_to_dataframe

DEFAULT_TEXT = "I am okay, but a little tired."


def analyze(user_text: str, alpha: float, face_image=None) -> dict[str, object]:
    """Run the full emotion pipeline for the demo."""

    text_probs = detect_text_emotion(user_text)
    text_backend_status = get_text_emotion_backend_status()
    face_probs = detect_face_emotion_from_image(face_image)
    face_warning = get_face_analysis_warning()
    fused_probs, fused_emotion = fuse_emotions(text_probs, face_probs, alpha)
    response = generate_response(user_text, fused_emotion)
    return {
        "text_probs": text_probs,
        "text_backend_status": text_backend_status,
        "face_probs": face_probs,
        "face_warning": face_warning,
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


def _probability_table(probs: dict[str, float]) -> object:
    """Build a display-ready probability table."""

    return probs_to_dataframe(probs)


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
        "pretrained transformer-based text emotion recognition when available, "
        "image-based facial emotion recognition, weighted fusion, and empathetic "
        "response generation."
    )

    with st.sidebar:
        st.header("Project Summary")
        st.write(
            "This prototype studies bimodal affective alignment by combining text "
            "and facial cues before generating a short supportive response."
        )
        st.write("Current stage: Day 6 Prototype")
        st.caption(
            "Day 6 uses a pretrained transformer-based text emotion module when available."
        )
        st.caption(
            "Image-based facial analysis remains part of the prototype."
        )

    uploaded_image = st.file_uploader(
        "Upload a facial image",
        type=["jpg", "jpeg", "png"],
        help="Optional: upload a face image for facial emotion analysis.",
    )
    uploaded_image_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    if uploaded_image_bytes is not None:
        st.image(uploaded_image_bytes, caption="Uploaded image preview", width="stretch")
    else:
        st.caption(
            "No image uploaded yet. The app will use a fallback facial distribution when you run analysis."
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
        if not user_text.strip():
            st.error("Please enter text before running analysis.")
            return

        results = analyze(user_text.strip(), alpha, uploaded_image_bytes)
        text_top = get_top_n_emotions(results["text_probs"], n=1)[0][0]
        face_top = get_top_n_emotions(results["face_probs"], n=1)[0][0]
        fused_top_3 = get_top_n_emotions(results["fused_probs"], n=3)

        st.markdown("### A) Text Emotion")
        st.dataframe(_probability_table(results["text_probs"]), width="stretch")
        text_backend_status = results["text_backend_status"]
        if text_backend_status["mode"] == "transformer":
            st.info(text_backend_status["message"])
        else:
            st.warning(text_backend_status["message"])
        _emotion_callout(st, text_top, "Text signal")

        st.markdown("### B) Face Emotion")
        st.dataframe(_probability_table(results["face_probs"]), width="stretch")
        if results["face_warning"]:
            st.warning(results["face_warning"])
        else:
            st.success("Facial analysis completed from the uploaded image.")
        _emotion_callout(st, face_top, "Face signal")

        st.markdown("### C) Fused Emotion")
        st.dataframe(_probability_table(results["fused_probs"]), width="stretch")
        top_3_frame = [
            {
                "Rank": rank,
                "Emotion": emotion.title(),
                "Probability": round(probability, 3),
            }
            for rank, (emotion, probability) in enumerate(fused_top_3, start=1)
        ]
        st.caption("Top 3 emotions from the fused distribution")
        st.dataframe(top_3_frame, width="stretch")

        st.markdown("### D) Final Detected Emotion")
        final_emotion = results["fused_emotion"]
        _emotion_callout(st, final_emotion, "Final detected emotion")
        st.metric("Detected emotion", final_emotion.title())

        st.markdown("### E) Empathetic Response")
        st.info(results["response"])

    st.divider()
    st.subheader("Prototype Evaluation Tools")
    st.caption(
        "Text-only = alpha 1.0, face-only = alpha 0.0, bimodal = alpha 0.5."
    )

    eval_col1, eval_col2 = st.columns(2)
    with eval_col1:
        if st.button("Run Ablation Study", key="run_ablation_study"):
            ablation_df = run_ablation_study(alpha=0.5)
            st.success(f"Saved ablation results to {ABLATION_RESULTS_PATH}")
            st.dataframe(ablation_df, width="stretch")
    with eval_col2:
        if st.button("Run Alpha Sensitivity", key="run_alpha_sensitivity"):
            alpha_df = run_alpha_sensitivity(DEFAULT_ALPHA_GRID)
            st.success(f"Saved alpha sensitivity results to {ALPHA_SENSITIVITY_PATH}")
            st.dataframe(alpha_df, width="stretch")

    st.divider()
    st.subheader("Human Evaluation and Case Studies")
    st.info(
        "Use a 1-5 scale to rate empathy, social presence, and trust. "
        "Case studies help compare congruent versus dissonant emotional signals."
    )

    human_col1, human_col2 = st.columns(2)
    with human_col1:
        if st.button(
            "Generate Human Evaluation Template",
            key="generate_human_eval_template",
        ):
            case_study_table = generate_case_study_table(alpha=0.5)
            template_table = make_human_eval_template(case_study_table)
            saved_path = save_human_eval_template(
                template_table,
                str(HUMAN_EVAL_TEMPLATE_PATH),
            )
            st.success(f"Saved human evaluation template to {saved_path}")
            st.dataframe(template_table, width="stretch")
    with human_col2:
        if st.button("Generate Case Study Table", key="generate_case_study_table"):
            case_study_table = generate_case_study_table(alpha=0.5)
            st.success(f"Saved case study table to {CASE_STUDIES_OUTPUT_PATH}")
            st.dataframe(case_study_table, width="stretch")


if __name__ == "__main__":
    main()

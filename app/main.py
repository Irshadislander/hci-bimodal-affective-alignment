"""Streamlit application for the bimodal affective alignment project."""

from __future__ import annotations

try:
    from app.face_emotion import (
        detect_face_emotion_from_image,
        get_face_analysis_warning,
        get_face_runtime_status,
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
    from app.final_evaluation_pack import (
        HUMAN_EVAL_SUMMARY_PATH,
        HUMAN_RATING_SHEET_COMPLETED_PATH,
        HUMAN_RATING_SHEET_PATH,
        MODE_COMPARISON_CASES_PATH,
        aggregate_human_ratings,
        build_human_rating_sheet,
        build_mode_comparison_cases,
        validate_completed_human_ratings,
    )
    from app.human_eval import (
        HUMAN_EVAL_TEMPLATE_PATH,
        make_human_eval_template,
        save_human_eval_template,
    )
    from app.fusion import get_top_n_emotions, fuse_emotions
    from app.response_generator import (
        generate_response,
        get_response_runtime_status,
    )
    from app.text_emotion import (
        detect_text_emotion,
        get_text_runtime_status,
    )
    from app.plot_results import plot_helpfulness_summary, plot_human_eval_summary
    from app.utils import probs_to_dataframe
except ImportError:  # pragma: no cover - supports running from app/ directly
    from face_emotion import (
        detect_face_emotion_from_image,
        get_face_analysis_warning,
        get_face_runtime_status,
    )
    from experiment_runner import (
        ABLATION_RESULTS_PATH,
        ALPHA_SENSITIVITY_PATH,
        DEFAULT_ALPHA_GRID,
        run_ablation_study,
        run_alpha_sensitivity,
    )
    from case_studies import CASE_STUDIES_OUTPUT_PATH, generate_case_study_table
    from final_evaluation_pack import (
        HUMAN_EVAL_SUMMARY_PATH,
        HUMAN_RATING_SHEET_COMPLETED_PATH,
        HUMAN_RATING_SHEET_PATH,
        MODE_COMPARISON_CASES_PATH,
        aggregate_human_ratings,
        build_human_rating_sheet,
        build_mode_comparison_cases,
        validate_completed_human_ratings,
    )
    from human_eval import (
        HUMAN_EVAL_TEMPLATE_PATH,
        make_human_eval_template,
        save_human_eval_template,
    )
    from fusion import get_top_n_emotions, fuse_emotions
    from response_generator import generate_response, get_response_runtime_status
    from text_emotion import detect_text_emotion, get_text_runtime_status
    from plot_results import plot_helpfulness_summary, plot_human_eval_summary
    from utils import probs_to_dataframe

DEFAULT_TEXT = "I am okay, but a little tired."


def analyze(user_text: str, alpha: float, face_image=None) -> dict[str, object]:
    """Run the full emotion pipeline for the demo."""

    text_probs = detect_text_emotion(user_text)
    text_runtime_status = get_text_runtime_status()
    face_probs = detect_face_emotion_from_image(face_image)
    face_warning = get_face_analysis_warning()
    face_runtime_status = get_face_runtime_status()
    fused_probs, fused_emotion = fuse_emotions(text_probs, face_probs, alpha)
    response = generate_response(user_text, fused_emotion)
    response_runtime_status = get_response_runtime_status()
    return {
        "text_probs": text_probs,
        "text_runtime_status": text_runtime_status,
        "text_backend_status": text_runtime_status,
        "face_probs": face_probs,
        "face_warning": face_warning,
        "face_runtime_status": face_runtime_status,
        "face_backend_status": face_runtime_status,
        "fused_probs": fused_probs,
        "fused_emotion": fused_emotion,
        "response": response,
        "response_runtime_status": response_runtime_status,
        "response_backend_status": response_runtime_status,
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


def _render_text_runtime_status(st, runtime_status: dict[str, object]) -> None:
    """Render a compact text-runtime status block for the analysis section."""

    runtime_mode = str(runtime_status.get("runtime_mode", "fallback_rule_based"))
    model_name = runtime_status.get("model_name") or "Unavailable"
    fallback_used = bool(runtime_status.get("fallback_used", False))
    reason = runtime_status.get("load_error") or runtime_status.get("inference_error")

    st.markdown("#### Text Runtime Status")
    status_cols = st.columns(2)
    status_cols[0].metric("Runtime mode", runtime_mode.replace("_", " ").title())
    status_cols[1].metric("Model", str(model_name))

    if fallback_used:
        if runtime_mode == "transformer" and runtime_status.get("transformer_active", False):
            st.warning(
                "The transformer runtime is active, but this analysis fell back "
                "to the emergency rule-based detector."
            )
        else:
            st.warning(
                "The transformer runtime was not available for this run, so the "
                "emergency rule-based fallback produced the text emotion distribution."
            )
        if reason:
            st.caption(f"Reason: {reason}")
    else:
        st.success(
            "The transformer runtime is active and provided the text emotion "
            "distribution for this run."
        )


def _render_face_runtime_status(
    st,
    runtime_status: dict[str, object],
    warning: str,
    has_image: bool,
) -> None:
    """Render a compact face-runtime status block for the analysis section."""

    runtime_mode = str(runtime_status.get("runtime_mode", "fallback_rule_based"))
    model_name = runtime_status.get("model_name") or "Unavailable"
    fallback_used = bool(runtime_status.get("fallback_used", False))
    face_runtime_active = bool(runtime_status.get("face_runtime_active", False))
    message = str(runtime_status.get("message", "")).strip()
    load_error = runtime_status.get("load_error")
    inference_error = runtime_status.get("inference_error")

    st.markdown("#### Face Runtime Status")
    status_cols = st.columns(2)
    status_cols[0].metric("Runtime mode", runtime_mode.replace("_", " ").title())
    status_cols[1].metric("Model", str(model_name))

    if warning:
        st.warning(warning)
    elif face_runtime_active and not fallback_used:
        st.success("Face inference is active and the uploaded image was analyzed directly.")
    elif face_runtime_active and fallback_used:
        if has_image:
            st.warning(
                "A backup face-analysis path was used for this run. "
                "The runtime remains active, but the primary model was not used."
            )
        else:
            st.warning(
                "No image was uploaded, so the safe fallback facial distribution was used."
            )
    else:
        st.info("The face runtime has not been activated yet.")

    if message and message != warning:
        st.caption(message)
    if load_error:
        st.caption(f"Load issue: {load_error}")
    if inference_error:
        st.caption(f"Analysis issue: {inference_error}")


def _render_response_runtime_status(st, runtime_status: dict[str, object]) -> None:
    """Render a compact response-runtime status block for the analysis section."""

    runtime_mode = str(runtime_status.get("runtime_mode", "fallback_template"))
    model_name = runtime_status.get("model_name") or "Unavailable"
    fallback_used = bool(runtime_status.get("fallback_used", False))
    response_runtime_active = bool(runtime_status.get("response_runtime_active", False))
    message = str(runtime_status.get("message", "")).strip()
    load_error = runtime_status.get("load_error")
    inference_error = runtime_status.get("inference_error")

    st.markdown("#### Response Runtime Status")
    status_cols = st.columns(2)
    status_cols[0].metric("Runtime mode", runtime_mode.replace("_", " ").title())
    status_cols[1].metric("Model", str(model_name))

    if response_runtime_active and not fallback_used:
        st.success("FLAN-T5 is active and generated the empathetic response for this run.")
    elif fallback_used:
        st.warning(
            "The response generator used the safe fallback path for this run."
        )
    else:
        st.info("The response runtime is not active yet.")

    if message:
        st.caption(message)
    if load_error:
        st.caption(f"Load issue: {load_error}")
    if inference_error:
        st.caption(f"Generation issue: {inference_error}")


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
        "A multimodal HCI prototype that uses transformer-first text emotion recognition "
        "with an emergency-only rule-based fallback, image-based facial emotion analysis, "
        "weighted fusion, and FLAN-T5-first empathetic response generation with a safe fallback."
    )

    with st.sidebar:
        st.header("Project Summary")
        st.write(
            "This project studies bimodal affective alignment by combining text "
            "and facial cues before generating a short supportive response."
        )
        st.write("Current status: Final evaluation package ready")
        st.caption(
            "Transformer-based text emotion analysis is the primary runtime; the rule-based fallback is reserved for failure recovery."
        )
        st.caption("Image-based facial analysis is enabled when an image is uploaded.")
        st.caption(
            "FLAN-T5 response synthesis is the primary runtime; the template fallback is reserved for generation failure."
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
            "No image has been uploaded. Facial analysis will use a neutral fallback distribution if you run analysis without an image."
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
        _render_text_runtime_status(st, results["text_runtime_status"])
        _emotion_callout(st, text_top, "Text emotion")

        st.markdown("### B) Face Emotion")
        st.dataframe(_probability_table(results["face_probs"]), width="stretch")
        _render_face_runtime_status(
            st,
            results["face_runtime_status"],
            results["face_warning"],
            uploaded_image_bytes is not None,
        )
        _emotion_callout(st, face_top, "Face emotion")

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
        _emotion_callout(st, final_emotion, "Final emotion")
        st.metric("Final emotion", final_emotion.title())

        st.markdown("### E) Empathetic Response")
        st.info(results["response"])
        _render_response_runtime_status(st, results["response_runtime_status"])

    st.divider()
    st.subheader("Evaluation Tools")
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
        "Use a 1-5 scale to rate empathy, social presence, trust, and helpfulness. "
        "The fused mode is the main system, while text-only and face-only serve as baselines."
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

    st.divider()
    st.subheader("Final Evaluation Pack")
    st.info(
        "Ask 4-8 people to rate empathy, social presence, trust, and helpfulness on a 1-5 scale. "
        "Fused mode is the main system; text_only and face_only are comparison baselines."
    )

    final_col1, final_col2, final_col3 = st.columns(3)
    with final_col1:
        if st.button("Generate Mode Comparison Cases", key="generate_mode_comparison_cases"):
            comparison_df = build_mode_comparison_cases(alpha=0.5)
            st.success(f"Saved mode comparison cases to {MODE_COMPARISON_CASES_PATH}")
            st.dataframe(comparison_df, width="stretch")
    with final_col2:
        if st.button("Generate Human Rating Sheet", key="generate_human_rating_sheet"):
            rating_df = build_human_rating_sheet(alpha=0.5)
            st.success(f"Saved human rating sheet to {HUMAN_RATING_SHEET_PATH}")
            st.dataframe(rating_df, width="stretch")
    with final_col3:
        if st.button("Aggregate Completed Human Ratings", key="aggregate_completed_human_ratings"):
            completed_path = HUMAN_RATING_SHEET_COMPLETED_PATH
            if not completed_path.exists():
                st.warning(
                    f"No completed human-rating file was found at {completed_path}. "
                    "A blank summary and placeholder plots will be generated."
                )
            validation_report = validate_completed_human_ratings(str(completed_path))
            summary_dict, summary_df = aggregate_human_ratings(str(completed_path))
            st.success(f"Saved human evaluation summary to {HUMAN_EVAL_SUMMARY_PATH}")
            st.caption(f"Aggregation status: {summary_dict.get('status')}")
            st.json(validation_report)
            st.dataframe(summary_df, width="stretch")
            summary_plot_path = plot_human_eval_summary(summary_df)
            helpfulness_plot_path = plot_helpfulness_summary(summary_df)
            st.caption(
                f"Saved plots to {summary_plot_path} and {helpfulness_plot_path}"
            )


if __name__ == "__main__":
    main()

# HCI Bimodal Affective Alignment

This project is a mini research-style Human-Computer Interaction system that combines:
- pretrained transformer-based text emotion recognition when available
- facial emotion recognition
- weighted emotion fusion
- empathetic response generation

## Project Goal
To build a bimodal affective alignment system that improves emotional understanding in human-computer interaction.

## Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run
./run.sh

## Facial Input
- Upload a face image in the Streamlit app to run image-based facial emotion analysis.
- If no image is uploaded, the app uses a safe neutral fallback distribution for the face signal.

## Text Emotion
- The app uses a pretrained HuggingFace text emotion model when available.
- If model loading fails, it falls back to the rule-based detector automatically.

## Running Evaluation Tools
- Open the Streamlit app and use the `Prototype Evaluation Tools` section.
- `Run Ablation Study` saves a fixed-alpha comparison across the default case set.
- `Run Alpha Sensitivity` saves a sweep across the default alpha grid.

## Human Evaluation Template Generation
- Open the Streamlit app and use the `Human Evaluation and Case Studies` section.
- `Generate Human Evaluation Template` builds a blank reviewer sheet with empathy, social presence, and trust fields.
- The template is based on the current case-study table and is ready for manual scoring.

## Case Study Generation
- `Generate Case Study Table` builds a compact set of congruent, dissonant, and ambiguous examples.
- The table is designed for report writing and presentation examples.
- Each row includes the text, text emotion, face emotion, fused emotion, and empathetic response.

## Final Human Evaluation Workflow
- Open the Streamlit app and use the `Final Human Evaluation Pack` section.
- `Generate Mode Comparison Cases` creates one row per case with text-only, face-only, and fused responses.
- `Generate Human Rating Sheet` creates a long-form reviewer sheet with blank rating fields.
- `Aggregate Completed Human Ratings` reads `experiments/human_rating_sheet_completed.csv`, validates it, and writes the summary table.
- Ask 4-8 raters to score empathy, social presence, trust, and helpfulness on a 1-5 scale.

## Generating Report Assets
- Run the evaluation tools first so the CSVs exist in `experiments/`.
- Load the saved CSVs with `app.report_assets` to compute a short report summary.
- Use `app.plot_results` to generate the report-ready PNG plots in `experiments/`.
- The first serious report draft is saved at `docs/final_report_draft.md`.
- The final presentation draft is saved at `docs/final_presentation_draft.md`.
- The demo script is saved at `docs/demo_script.md`.
- The results-summary draft is saved at `docs/results_summary_draft.md`.

## CSV Outputs
- Ablation results are saved to `experiments/ablation_results.csv`
- Alpha sensitivity results are saved to `experiments/alpha_sensitivity.csv`
- Human evaluation templates are saved to `experiments/human_eval_template.csv`
- Case study tables are saved to `experiments/case_studies.csv`
- Mode comparison cases are saved to `experiments/mode_comparison_cases.csv`
- Human rating sheets are saved to `experiments/human_rating_sheet.csv`
- Completed human rating sheets are read from `experiments/human_rating_sheet_completed.csv`
- Human evaluation summaries are saved to `experiments/human_eval_summary.csv`
- Human evaluation plots are saved to `experiments/human_eval_summary_plot.png` and `experiments/helpfulness_summary_plot.png`
- Plot outputs are saved to `experiments/ablation_counts.png`, `experiments/alpha_sensitivity_plot.png`, and `experiments/case_type_distribution.png`

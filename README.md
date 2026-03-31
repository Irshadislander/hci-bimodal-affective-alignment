# HCI Bimodal Affective Alignment

## 1. Project Title
HCI Bimodal Affective Alignment is a multimodal Human-Computer Interaction project that combines text emotion analysis, facial emotion analysis, weighted fusion, and empathetic response generation in a transparent research prototype.

## 2. Overview
This repository contains a compact academic prototype for studying whether a bimodal affective pipeline can produce more interpretable and socially useful emotion-aware interaction than unimodal baselines. The system accepts user text and an uploaded facial image, estimates emotion probabilities for each modality, fuses the results, and generates a short supportive response.

The project is designed for both demonstration and evaluation. The Streamlit application presents the live interaction flow, while the supporting modules generate report-ready CSV tables, plots, human-rating sheets, case studies, and presentation assets.

## 3. Motivation
Emotion-aware interfaces often receive incomplete or ambiguous signals from a single input channel. Text can be expressive but missing visual context, while facial cues can be informative but unavailable or noisy. This project studies a transparent weighted-fusion baseline that keeps the decision process easy to inspect, explain, and evaluate in an HCI setting.

## 4. System Architecture
The system is organized into small modules with clear responsibilities:
- `app/text_emotion.py` for transformer-first text emotion runtime
- `app/face_emotion.py` for image-based facial emotion analysis, with DeepFace as the primary runtime and a safe fallback only when face loading or detection fails
- `app/fusion.py` for weighted late fusion
- `app/response_generator.py` for FLAN-T5-first empathetic response generation with a safe fallback
- `app/evaluation.py`, `app/experiment_runner.py`, `app/case_studies.py`, `app/human_eval.py`, and `app/final_evaluation_pack.py` for evaluation assets
- `app/report_assets.py`, `app/plot_results.py`, and `app/final_report_builder.py` for report and presentation outputs
- `app/main.py` for the Streamlit interface

## 5. Core Capabilities
- Transformer-first text emotion analysis with emergency-only rule-based fallback
- Image-based facial emotion analysis with DeepFace as the primary runtime and safe fallback only for failure recovery
- Weighted fusion across the seven emotion classes
- FLAN-T5-first empathetic response generation with fallback only for load or generation failure
- Ablation study support
- Alpha sensitivity analysis
- Case-study generation
- Human evaluation template and aggregation support
- Report and presentation asset generation

## 6. Evaluation Workflow
The repository includes a structured evaluation pipeline for the final course submission:
- fixed-alpha ablation study
- alpha sensitivity sweep
- case-study generation
- mode comparison tables
- human evaluation templates and summaries
- report tables and report status exports

These outputs are saved under `experiments/` and reused in the report and presentation drafts.

## 7. Repository Structure
```text
hci-bimodal-affective-alignment/
├── app/                  # Streamlit app, model helpers, evaluation utilities, report builders
├── docs/                 # Report drafts, presentation drafts, instructions, and project references
├── experiments/          # Generated CSV files and PNG plots
├── tests/                # Offline-safe smoke tests
├── README.md             # Project overview and usage guide
└── run.sh                # Convenience script for launching the app
```

## 8. Setup
Create the environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you prefer a single launch command after the environment is ready:

```bash
./run.sh
```

## 9. Running the Application
Launch the Streamlit demo directly:

```bash
streamlit run app/main.py
```

For a headless local check:

```bash
streamlit run app/main.py --server.headless true --browser.gatherUsageStats false --server.port 8501
```

## 10. Human Evaluation Workflow
Use `docs/human_rating_instructions.md` before collecting ratings.

Recommended workflow:
1. Generate `experiments/human_rating_sheet.csv` from the app.
2. Share the sheet with each evaluator.
3. Ask each evaluator to keep one consistent `rater_id` across all rows.
4. Collect completed ratings in `experiments/human_rating_sheet_completed.csv`.
5. Run `Aggregate Completed Human Ratings` in the app to produce `experiments/human_eval_summary.csv` and the corresponding plots.
6. Treat `Text only`, `Face only`, and `Fused` as the comparison modes in the sheet.

The rating dimensions are:
- empathy
- social presence
- trust
- helpfulness

Each dimension is rated on a 1-5 scale.

## 11. Report and Presentation Assets
The repository includes a complete documentation package for the final submission:
- `docs/final_report_draft.md`
- `docs/report_tables.md`
- `docs/report_status.md`
- `docs/final_presentation_draft.md`
- `docs/demo_script.md`
- `docs/results_summary_draft.md`
- `docs/project_overview.md`
- `docs/current_status.md`
- `docs/repository_guide.md`
- `docs/final_artifacts_index.md`
- `docs/final_report_submission_checklist.md`
- `docs/human_rating_instructions.md`

## 12. Generated Outputs
Key generated files are stored as follows:
- `experiments/ablation_results.csv`
- `experiments/alpha_sensitivity.csv`
- `experiments/case_studies.csv`
- `experiments/mode_comparison_cases.csv`
- `experiments/human_rating_sheet.csv`
- `experiments/human_rating_sheet_completed.csv`
- `experiments/human_eval_summary.csv`
- `experiments/ablation_counts.png`
- `experiments/alpha_sensitivity_plot.png`
- `experiments/case_type_distribution.png`
- `experiments/human_eval_summary_plot.png`
- `experiments/helpfulness_summary_plot.png`
- `docs/report_tables.md`
- `docs/report_status.md`

## 13. Current Status
The full pipeline is implemented and the application runs end to end. The repository already contains the text emotion module, face emotion module, fusion layer, response generator, evaluation workflows, case studies, human evaluation template, report draft, presentation draft, demo script, report tables, and report status exports.

The remaining manual step is to collect completed human ratings, aggregate them, and insert the resulting averages into the final report if the evaluation is conducted before submission.

## 14. Future Extensions
The current prototype is a strong baseline, and it can be extended in several directions:
- replace fallback text and facial logic with stronger models if needed
- improve calibration and confidence reporting
- support richer human evaluation studies
- explore additional modalities or datasets
- refine response generation for deeper interaction studies

# Repository Guide

## `app/`
Core application code for the Streamlit demo and supporting analysis utilities.

Typical contents:
- `main.py` for the Streamlit interface
- `text_emotion.py`, `face_emotion.py`, `fusion.py`, and `response_generator.py` for the main pipeline
- `evaluation.py`, `experiment_runner.py`, `case_studies.py`, `human_eval.py`, and `final_evaluation_pack.py` for evaluation assets
- `report_assets.py`, `plot_results.py`, and `final_report_builder.py` for report outputs

## `docs/`
Documentation, report drafts, presentation drafts, and project-facing references.

Typical contents:
- final report and presentation drafts
- demo script and submission checklist
- human-rating instructions
- report tables and report status summaries
- project overview, repository guide, and final artifacts index

## `experiments/`
Generated evaluation outputs and plots.

Typical contents:
- ablation and alpha sensitivity CSV files
- case-study tables
- human rating sheets and human evaluation summaries
- PNG plots used in the report and presentation

## `tests/`
Offline-safe smoke tests for the main pipeline and report utilities.

Typical contents:
- module import checks
- smoke tests for text, face, fusion, and response generation
- evaluation and report-builder tests

## `README.md`
High-level project documentation for GitHub.

It explains the architecture, setup, runtime commands, evaluation workflow, and key output locations.

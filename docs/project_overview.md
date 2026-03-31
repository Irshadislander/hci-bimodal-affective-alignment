# Project Overview

HCI Bimodal Affective Alignment is a research-oriented Human-Computer Interaction project for studying whether text emotion signals and facial emotion signals can be combined into a more useful affective interpretation.

The system includes:
- a transformer-first text emotion classifier with a rule-based fallback
- image-based facial emotion analysis with safe fallback behavior
- weighted late fusion over seven emotion classes
- short empathetic response generation
- evaluation workflows for ablation, alpha sensitivity, case studies, and human ratings

The project is intentionally designed as a transparent research scaffold. The codebase keeps the model stages modular, exposes the evaluation utilities directly in the app, and writes all report-ready artifacts to disk so they can be reused in the final submission.

Primary outputs include:
- CSV tables for ablation, alpha sensitivity, case studies, mode comparison, and human evaluation
- matplotlib plots for experiment summaries
- a written report draft
- a presentation draft and demo script

The overall research question is whether a simple bimodal fusion strategy can improve the quality and interpretability of emotion-aware interaction compared with unimodal baselines.

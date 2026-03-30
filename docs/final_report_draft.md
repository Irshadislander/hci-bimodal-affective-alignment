# HCI Bimodal Affective Alignment: A Mini Research Prototype for Multimodal Emotion-Aware Interaction

## Abstract
This project investigates whether a lightweight bimodal affective pipeline can improve the quality of emotion-aware interaction in a small HCI prototype. The system combines a pretrained transformer-based text emotion classifier, an image-based facial emotion module, a weighted late-fusion rule, and a short empathetic response generator. The implementation is intentionally modular so that each component can be examined independently and then compared in text-only, face-only, and fused settings. The current report draft focuses on how the prototype is built and how it will be evaluated, while leaving measured results to be inserted from the generated experiment CSVs and plots. In particular, the project is designed to support ablation analysis, alpha sensitivity analysis, case-study comparison, and a compact human-evaluation workflow using empathy, social presence, and trust ratings.

## 1. Introduction and Motivation
Emotion-aware interaction is a recurring problem in human-computer interaction because user input often carries signals that are not captured by a single modality. Text alone can miss tone and nonverbal context, while facial cues alone can be ambiguous or unavailable. This project explores a simple but research-oriented response to that problem: combine text and face information into one fused affect estimate, then generate a short response that is aligned with the final emotion prediction.

The prototype is intentionally framed as a mini research system rather than a production-ready emotion engine. That framing matters because the goal is not to claim state-of-the-art recognition performance; instead, the goal is to build a clear experimental scaffold that can support a final course project. The system is designed to be inspectable, easy to demo, and easy to evaluate with a small set of controlled cases.

## 2. Research Question
The central research question is whether a lightweight bimodal fusion strategy can improve the perceived quality of emotion-aware responses in a prototype HCI setting. A secondary question is how the fusion weight, alpha, changes the final emotion prediction when the text and face signals agree or conflict.

This question is practical rather than clinical. The prototype is meant to help answer whether a simple weighted fusion pipeline is understandable, useful, and expressive enough for a course project demo. The resulting report will compare text-only, face-only, and fused interpretations so that the contribution of multimodal combination is visible rather than assumed.

## 3. System Overview
The system accepts a short text message and an image-based facial signal, runs emotion analysis on each modality, fuses the resulting probability distributions, and produces a short empathetic response. In the current implementation, the text module uses a pretrained transformer when available and falls back to a rule-based detector when necessary. The face module analyzes uploaded images with DeepFace and uses a safe fallback distribution when no image is provided or face analysis fails.

The Streamlit application is organized to support this workflow directly. The main interface shows the text probabilities, face probabilities, fused probabilities, top fused emotions, and the final response. In addition, the app exposes experimental utilities for ablation studies, alpha sensitivity, human-evaluation template generation, and case-study generation. These assets are saved to the `experiments/` directory so that they can be reused in the report and presentation.

## 4. Technical Methodology
The text emotion module estimates probabilities over seven emotions: happy, sad, angry, neutral, fear, surprise, and disgust. When the pretrained Hugging Face model is available, the pipeline maps its output labels into the project schema and normalizes the resulting distribution. If the model cannot be loaded or inference fails, the module falls back to a lexical scoring method that still returns a normalized probability vector.

The facial module follows a similar philosophy of graceful degradation. When an image is available, it attempts image-based analysis and maps the resulting emotion scores into the same seven-emotion schema. When the image is missing or analysis is unavailable, the system returns a safe neutral-leaning distribution rather than failing. This makes the prototype stable enough for demo use while still preserving the intended bimodal structure.

## 5. Fusion Strategy
The fusion strategy uses a weighted late-fusion rule over the aligned emotion probabilities. For each emotion `e`, the fused score is computed as `Fused(e) = alpha * Text(e) + (1 - alpha) * Face(e)`, where alpha controls the relative influence of the text modality. The final detected emotion is the argmax of the fused distribution.

This formulation is intentionally simple because the project is trying to make the decision process interpretable. Text-only evaluation corresponds to `alpha = 1.0`, face-only evaluation corresponds to `alpha = 0.0`, and bimodal fusion is typically presented at `alpha = 0.5`. The report will use this setup to discuss how the model behaves when the two modalities agree, disagree, or provide only weak evidence.

## 6. System Implementation
The codebase is structured as a small research prototype with separate modules for text emotion detection, facial emotion analysis, fusion, response generation, evaluation, case studies, and report assets. This separation is useful because it makes each stage of the pipeline easier to test and easier to explain in the report. The Streamlit app acts as the main interface, but the same functions are also usable from scripts and tests.

The implementation also saves experiment outputs into the `experiments/` directory. The ablation study writes `ablation_results.csv`, the alpha sweep writes `alpha_sensitivity.csv`, the case-study workflow writes `case_studies.csv`, and the human-evaluation helper writes `human_eval_template.csv`. Report-oriented plots are written as PNG files in the same directory. These generated files are the main source for the final report figures and tables.

## 7. Experimental Setup
The evaluation setup is designed around three complementary artifacts: a fixed-alpha ablation study, an alpha sensitivity sweep, and a compact case-study table. The ablation study compares text-only, face-only, and fused interpretations across a curated set of sample texts. The alpha sweep reuses the same cases over a grid of alpha values so that changes in the fused prediction can be tracked systematically.

The human-evaluation workflow is separate from the automatic experiments. It creates a review template with columns for empathy, social presence, trust, and notes, using a 1-5 rating scale for the qualitative judgments. The case-study workflow generates examples that are intentionally congruent, dissonant, or ambiguous, which makes them useful both for discussion in the report and for presentation slides. Where actual measured values are unavailable in this draft, the report will insert the generated CSV outputs and their derived plots.

## 8. Ablation Study
The ablation study is the most direct way to show what each modality contributes. Text-only results show how the system behaves when alpha is set to 1.0, face-only results show the opposite extreme, and fused results show the intermediate behavior of the bimodal design. In the report, this section should explain whether fusion changes the top emotion and whether it produces a more plausible interpretation than either modality alone.

The generated ablation CSV is intended to support a compact table of representative cases as well as a simple bar chart of fused emotion counts. The actual values will be inserted from the generated experiment CSVs, and the discussion should focus on the pattern of agreement or disagreement across the modalities rather than on a single headline number. This section should also note any cases where the fusion result is effectively driven by one modality because the other modality is uncertain or close to neutral.

## 9. Alpha Sensitivity
Alpha sensitivity is used to make the weighting behavior visible. By sweeping alpha across a small grid, the project can show how the final emotion shifts when the model trusts text more or face more. This is particularly useful for mixed or dissonant cases because a slight weight change can sometimes alter the final interpretation.

The report should use the generated alpha sensitivity plot to show the trend rather than to overclaim precision. The important question is not whether one alpha value is universally best, but whether the system behaves in a stable and explainable way across a small set of representative examples. Results will be inserted from the generated experiment CSVs, and the discussion should highlight stable cases, sensitive cases, and the role of the face fallback distribution in offline evaluation.

## 10. Human Evaluation Plan
The human-evaluation plan is intended to assess the prototype from a user-centered perspective rather than only from an algorithmic one. Reviewers will see case-level outputs and rate the response on empathy, social presence, and trust using a 1-5 scale. The template generated by the project is designed to make this process lightweight and consistent across cases.

The report should explain that the human evaluation is meant to compare the perceived quality of text-only, face-only, and fused outputs. Even though this is a small course-project setup, the comparison is useful because it aligns the technical fusion strategy with the human experience of the system. The evaluation plan should also mention that the current version is prototype-level and does not claim clinical validity or broad generalization.

## 11. Case Studies
Case studies help make the system behavior concrete. A good case-study set should include congruent examples, where text and face suggest the same emotion; dissonant examples, where the signals conflict; and ambiguous examples, where both signals are weak or mixed. These cases can be used to explain why the fused decision was chosen and whether the final response feels appropriately supportive.

The case-study table generated by the project is intended for both the report and the presentation. It records the user text, the top emotion from each modality, the fused emotion, the response, and a case type label. In the final report, this section should present a small table or set of narrative examples that show how the prototype behaves in different emotional conditions, especially when text and facial cues disagree.

## 12. Results and Discussion
This section should synthesize the outputs of the experiments and the case-study workflow. The report should describe what the ablation study suggests about modality contribution, what the alpha sweep suggests about weight sensitivity, and what the case studies suggest about qualitative alignment. The goal is to interpret the system behavior in a way that is readable to a human evaluator, not just to summarize tables mechanically.

At this stage of the project, the detailed numerical results will be inserted from the generated experiment CSVs and plots. The discussion should therefore focus on patterns: when the fused model appears stable, when one modality dominates, when the response generator feels appropriately supportive, and when the prototype exposes limitations in the underlying emotion signals. This is also the section where the strongest and most informative case studies should be referenced explicitly.

## 13. Limitations
The current prototype has several clear limitations that should be stated directly. The text module is still a lightweight classifier with a fallback rule-based path, the face module relies on image upload rather than live interaction, and the response generator uses short templates instead of a learned conversational model. These choices are acceptable for a course project, but they limit realism and external validity.

Another limitation is that the evaluation data are intentionally small and curated. The system is good for demonstrating design ideas, but it is not a benchmark for general emotion recognition performance. The final report should also note that the human evaluation is exploratory and that the face signal is evaluated in a controlled prototype setting rather than a naturalistic deployment.

## 14. Future Work
The most obvious next step is to replace the remaining approximate components with stronger learned models. For text, that could mean a more carefully calibrated classifier or a domain-specific model. For face, that could mean live webcam input or a more robust facial affect model with confidence calibration. For response generation, that could mean a richer empathetic dialogue policy rather than template selection.

A second direction is to broaden the evaluation. The current human-evaluation plan is intentionally lightweight, but a larger study could compare response quality across more cases and more participants. A third direction is to improve interpretability by adding confidence visualization, calibration curves, and explicit disagreement handling so that the system can explain why a fused emotion was chosen.

## 15. Conclusion
This project shows how a small HCI prototype can be structured as a research scaffold for multimodal affective alignment. By separating text emotion recognition, facial emotion analysis, weighted fusion, and empathetic response generation into clean modules, the system makes it possible to study how each component contributes to the final interaction.

The broader contribution of the project is not a claim of performance but a clear and extensible workflow for experimentation, human evaluation, and report writing. The generated CSVs, plots, case studies, and templates are meant to support the final course submission, while the current implementation provides a stable foundation that the team can continue refining.

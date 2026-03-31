# HCI Bimodal Affective Alignment: A Research Prototype for Multimodal Emotion-Aware Interaction

## Abstract
This project investigates whether a lightweight bimodal affective pipeline can improve the quality and interpretability of emotion-aware interaction in an HCI setting. The system combines a pretrained transformer-based text emotion classifier, an image-based facial emotion module, a weighted late-fusion rule, and a short empathetic response generator. The prototype is intentionally modular so that each stage can be examined independently and compared in text-only, face-only, and fused settings.

The main contribution of the project is not a claim of state-of-the-art recognition accuracy. Instead, it is a research-style scaffold that supports controlled comparisons, report-ready visualizations, and a small human-evaluation workflow. The evaluation package includes ablation analysis, alpha sensitivity analysis, case studies, and a rating sheet for empathy, social presence, trust, and helpfulness. If completed human ratings are available at submission time, their final averages will be inserted after data collection and aggregation.

## 1. Introduction and Motivation
Emotion-aware interaction matters in HCI because users rarely communicate affect through a single channel. A short message can sound polite while still carrying frustration, and a face can look neutral even when the accompanying text is emotionally loaded. A unimodal system therefore risks being correct in a narrow technical sense while still missing the user’s actual state. That ambiguity is especially important in a course project, where the system should be understandable to humans rather than optimized only for a benchmark.

This project is built around that observation. It asks whether a simple multimodal design can better align the system’s interpretation with the signals that a human observer would expect. The codebase is small enough to inspect end to end, but it still exposes the key design choices that make multimodal HCI systems interesting: modality reliability, disagreement, fallback behavior, and the effect of weighting on the final decision.

## 2. Research Question
The central research question is whether a lightweight bimodal fusion strategy can produce more aligned emotion estimates and more human-centered responses than either modality alone. A closely related question is how the fusion weight, alpha, changes the final prediction when the text and face signals agree, partially agree, or conflict.

This comparison matters because a fused output is only meaningful if the baselines are visible. Text-only and face-only results make it possible to see whether fusion adds value, smooths over noise, or simply follows the strongest modality. In other words, the baselines protect the interpretation of the fused model and keep the report grounded in observable behavior rather than assumption.

## 3. System Overview
The system accepts a short text message and an uploaded facial image, analyzes both modalities, combines the resulting probability distributions, and generates a short empathetic response. The text path uses a pretrained Hugging Face model when available and falls back to a deterministic lexical detector when it is not. The face path uses DeepFace on uploaded images and falls back to a safe neutral-leaning distribution when the image is missing or facial analysis fails.

The Streamlit application presents the full pipeline in a single interface so that the system can be demonstrated, inspected, and evaluated without extra tooling. In addition to the live demo path, the app exposes batch utilities for ablation studies, alpha sweeps, case studies, human-evaluation sheet generation, and final evaluation pack generation. All experiment outputs are written to `experiments/` so that the report and presentation can reference the exact same artifacts.

## 4. Technical Methodology
The text emotion module predicts probabilities over seven emotions: happy, sad, angry, neutral, fear, surprise, and disgust. When the transformer backend is available, its labels are mapped into the project schema and normalized to a probability distribution. When the backend is unavailable, the module falls back to a rule-based scoring method that still produces a normalized seven-class output. This design keeps the text path stable for offline use while still prioritizing a stronger pretrained model when possible.

The face module follows the same principle of graceful degradation. When an image is present, the system attempts image-based emotion analysis and maps the result into the same seven-emotion schema used by the text module. When image analysis cannot proceed, the module returns a safe fallback distribution that is mostly neutral. This ensures that the rest of the prototype can continue operating even in a constrained demo environment.

Both modalities are normalized before fusion. That step matters because the fusion equation assumes comparable probability mass across the two inputs. Without normalization, the model could give one modality undue influence for implementation reasons rather than because it is more informative.

## 5. Fusion Strategy
The fusion layer uses a simple weighted average over aligned emotion probabilities. For each emotion `e`, the fused score is computed as `Fused(e) = alpha * Text(e) + (1 - alpha) * Face(e)`. The resulting fused distribution is then converted into a final emotion label using the highest probability score.

This strategy is intentionally transparent. It allows the report to discuss the effect of alpha directly and makes it easy to compare three operating points: text-only at `alpha = 1.0`, face-only at `alpha = 0.0`, and balanced bimodal fusion at `alpha = 0.5`. The weighted formulation is also appropriate for a course project because it exposes disagreement between modalities instead of hiding it inside a more opaque model.

The value of fusion becomes clearest when the modalities are ambiguous or partially inconsistent. A text message may be emotionally positive while the face appears tense, or the face may look neutral while the text indicates distress. In those cases, the fused output provides a principled compromise that can be evaluated against the unimodal baselines and judged by human raters.

## 6. System Implementation
The codebase is organized into small modules for text emotion detection, facial emotion analysis, fusion, response generation, evaluation, case studies, and report assembly. This separation keeps the prototype maintainable and makes the logic easy to explain during a presentation. It also helps with testing, because each stage can be exercised independently without having to run the full app.

The implementation writes results into `experiments/` and the documentation package into `docs/`. The ablation study, alpha sensitivity sweep, mode-comparison sheet, human-rating sheet, and human-evaluation summary all have explicit file paths, which makes it possible to rerun or inspect the exact outputs later. That structure is important for a final course submission because the report can point directly to the generated tables and plots instead of relying on manual recreation.

## 7. Experimental Setup
The experimental package is built around three complementary views of the same prototype. The first is a fixed-alpha ablation study that compares text-only, face-only, and fused outputs over a curated set of cases. The second is an alpha sensitivity sweep that shows how the fused label changes as the text-face weight shifts. The third is a case-study table that presents representative congruent, dissonant, and ambiguous examples in a format suitable for the report and presentation.

The human-evaluation workflow is separate from the automatic experiments because it measures a different kind of success. Rather than asking whether the classifier is internally consistent, it asks whether the output feels empathetic, socially present, trustworthy, and helpful to a human reader. The current template uses a 1-5 scale and is intended for a small group of raters. If completed ratings are not yet available, the report can state that the final human-rating averages will be inserted after data collection and aggregation.

## 8. Ablation Study
The ablation study is the most direct comparison of the three system modes. Text-only results show what the prototype believes when it trusts the language input completely. Face-only results show the opposite extreme. Fused results show the effect of combining the modalities with a shared decision rule. This makes the ablation section central to the report, because it demonstrates whether fusion adds interpretive value or merely reproduces one of the baselines.

The ablation CSV and its derived plot show how often each fused emotion appears across the case set. More importantly, the discussion interprets representative cases. If the fused prediction agrees with both modalities, that supports the basic design. If it resolves a disagreement sensibly, that is evidence that the bimodal design is doing useful work. If it simply tracks the strongest modality every time, that is also informative because it suggests the current weighting scheme is conservative.

## 9. Alpha Sensitivity
Alpha sensitivity is included to show how robust the fused decision is to weighting. A stable prototype does not change wildly when alpha moves slightly, especially in cases where both modalities carry similar evidence. At the same time, a meaningful bimodal system should show that alpha matters when the signals conflict or when one modality is weak.

The report presents alpha sensitivity as a transparency tool rather than a tuning exercise. The point is not to claim that one alpha value is universally optimal. The point is to show how the final prediction behaves across a small grid and to identify stable cases, sensitive cases, and cases where the face fallback distribution effectively leaves the text signal in control. Results are inserted from the generated experiment CSVs and the corresponding plot.

## 10. Human Evaluation Plan
The human-evaluation plan is designed to assess the prototype from an HCI perspective rather than only from a machine-learning perspective. Reviewers will read the case-level outputs and rate empathy, social presence, trust, and helpfulness on a 1-5 scale. These dimensions matter because a supportive response can still feel cold, vague, or untrustworthy even if the emotion label is technically plausible.

This evaluation also strengthens the credibility of the report. Because the fused output is the main system, it is judged by the human qualities that matter in interaction design. A small rating study cannot prove general effectiveness, but it can show whether the prototype produces outputs that people can understand and evaluate consistently. If completed ratings are not yet available, the report states that the final human-rating averages will be inserted after data collection and aggregation.

## 11. Case Studies
Case studies help make the prototype concrete. Congruent cases are useful because they show the system when text and face reinforce one another. Dissonant cases are particularly valuable because they reveal how the system behaves when the cues disagree. Ambiguous cases show what the prototype does when both modalities are weak or mixed. Together, these examples support a more nuanced discussion than a single aggregate score would allow.

The case-study table generated by the project records the user text, the top emotion from each modality, the fused emotion, the response, and a case type label. In the final report, this section highlights a small number of examples that illustrate different interaction patterns. The goal is to show how the prototype handles emotionally consistent input, conflicting signals, and borderline input where the system should avoid overconfidence.

## 12. Results and Discussion
The results and discussion section synthesizes the outputs of the automatic experiments, the case studies, and the human evaluation. The report explains what the ablation study says about modality contribution, what the alpha sweep says about robustness, and what the case studies say about interpretability. The discussion also remains clear about where the prototype behaves well and where it still depends heavily on fallback behavior or simple heuristics.

At the time of writing, the exact numbers are inserted from the generated CSVs and plots. If the completed human-rating file is available, the final human-rating averages are inserted after data collection and aggregation. If not, the report clearly states that the human-evaluation template and aggregation workflow are ready, but the completed scores were not yet available. Either way, the discussion remains factual and grounded in the generated artifacts.

## 13. Limitations
This prototype has clear limitations, and they are stated directly. The text module still includes a fallback path, the face module relies on uploaded images instead of live capture, and the response generator uses short template-based outputs rather than a learned dialogue policy. These choices are appropriate for a course project, but they limit realism and make the system less robust than a production-grade affective interface.

The evaluation design is also intentionally small. The curated cases are useful for demonstrating the system and for writing a coherent report, but they are not a substitute for a large user study or a benchmark evaluation. The project is therefore best described as a research scaffold: strong enough to support meaningful discussion, but not a claim of general-purpose emotion understanding.

## 14. Future Work
The most immediate future work is to improve the individual modalities. For text, that could mean a stronger classifier or better calibration. For face, that could mean live webcam capture, improved face detection, or a more robust facial affect model. For response generation, that could mean a richer conversational policy that adapts to context instead of selecting from short templates.

A second direction is to strengthen the evaluation. The current human-evaluation workflow is a useful course-project baseline, but a larger participant pool and a more formal protocol would make the results more convincing. A third direction is to make disagreement more interpretable by exposing confidence, calibration, or an explicit explanation for why the fused emotion was chosen.

## 15. Conclusion
The project demonstrates how a small HCI prototype can be structured as a multimodal affective-alignment system. By separating text emotion recognition, facial emotion analysis, weighted fusion, and empathetic response generation into clean modules, the prototype provides a transparent setting for comparing unimodal and fused behavior.

The broader contribution is methodological rather than statistical. The system gives the team a complete workflow for experimentation, case studies, human evaluation, and report generation. That makes it a practical foundation for the final course submission and a credible starting point for future HCI work on emotion-aware interaction.

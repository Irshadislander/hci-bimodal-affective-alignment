# Presentation Outline

## 1. Title
- Project title and one-line framing.
- Presenter, course, and date.
- Speaker notes: introduce the project as a Day 8 multimodal affective-alignment prototype.

## 2. Motivation
- Why emotion-aware HCI matters.
- Why a bimodal prototype is worth building.
- Speaker notes: frame the problem around better interpretation of user state.

## 3. Problem Statement
- Why single-modality emotion signals are fragile.
- Why a simple weighted fusion layer is a practical baseline.
- Speaker notes: explain the mismatch between text-only and face-only signals.

## 4. Research Question
- State the main research question.
- Mention alpha sensitivity as the weighting question.
- Speaker notes: define the research goal as comparing unimodal and fused behavior.

## 5. System Architecture
- Show the end-to-end pipeline diagram.
- Introduce the Streamlit demo flow.
- Speaker notes: point out the report-ready workflow and saved experiment artifacts.

## 6. Text Emotion Module
- Summarize the transformer-first text emotion path.
- Mention the rule-based fallback.
- Speaker notes: note that this module runs on seven emotion classes.

## 7. Face Emotion Module
- Summarize the image-based face emotion path.
- Mention the fallback distribution when no face or image is available.
- Speaker notes: clarify that this is image-based, not webcam-based, for the current prototype.

## 8. Fusion Strategy
- Show the weighted fusion equation.
- Explain what alpha does.
- Speaker notes: contrast text-only, face-only, and fused modes.

## 9. Response Generation
- Show the empathetic-response layer.
- Explain how the response depends on the fused emotion.
- Speaker notes: emphasize that the responses are short, supportive, and demo-safe.

## 10. Ablation Study
- Show the ablation table or compact summary plot.
- Compare text-only, face-only, and fused outputs.
- Speaker notes: place `experiments/ablation_counts.png` here and explain when fusion changes the top emotion.

## 11. Alpha Sensitivity
- Show the alpha sensitivity plot.
- Explain how alpha shifts the fused emotion.
- Speaker notes: place `experiments/alpha_sensitivity_plot.png` here and call out stable versus sensitive cases.

## 12. Human Evaluation
- Show the human-evaluation template and summary table.
- Explain the 1-5 scales for empathy, social presence, trust, and helpfulness.
- Speaker notes: briefly summarize the current result pattern if completed ratings exist, or note that the CSV will be filled by raters.

## 13. Case Studies
- Show the case-study table.
- Include one congruent, one dissonant, and one ambiguous example.
- Speaker notes: place `experiments/case_studies.csv` here or a clipped table derived from it.

## 14. Limitations and Future Work
- Mention the current technical limitations.
- Mention the evaluation scope and what remains to be done.
- Speaker notes: end with a clear statement of what still needs improvement and why.

## 15. Conclusion
- Restate the main takeaway.
- Reinforce the value of the prototype as a research scaffold.
- Speaker notes: close by tying the project back to multimodal affective alignment in HCI.

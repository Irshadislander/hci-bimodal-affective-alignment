# Report Outline

## Title
- Confirm the final paper title and subtitle.
- Decide how to frame the prototype as a course-project contribution.
- Keep the title aligned with the report draft and presentation.

## Abstract
- State the problem, the bimodal approach, and the main evaluation artifacts.
- Mention text emotion, face emotion, fusion, and empathetic response generation.
- Note that the report is a draft backed by generated CSVs and plots.

## 1. Introduction and Motivation
- Why does emotion-aware interaction matter in HCI?
- Why are text and facial cues useful together?
- What makes this project a small but meaningful research prototype?

## 2. Research Question
- Write the main question in one sentence.
- Add the alpha-sensitivity subquestion.
- Explain why the question fits a mini research project.

## 3. System Overview
- Describe the end-to-end pipeline from input to response.
- Summarize the role of the Streamlit interface.
- Mention the report-ready experimental workflow.

## 4. Technical Methodology
- Describe the text emotion path and fallback behavior.
- Describe the image-based face emotion path and fallback behavior.
- Explain how probabilities are normalized before fusion.

## 5. Fusion Strategy
- Write the weighted fusion equation.
- Explain what alpha means in practice.
- Compare text-only, face-only, and bimodal settings.

## 6. System Implementation
- List the main modules in the codebase.
- Explain how CSVs and plots are saved under `experiments/`.
- Mention the separation between demo logic and evaluation logic.

## 7. Experimental Setup
- Describe the ablation study inputs and outputs.
- Describe the alpha sensitivity sweep.
- Describe the case-study and human-evaluation artifacts.

## 8. Ablation Study
- Explain what text-only, face-only, and fused outputs show.
- Identify which plot or table will appear here.
- Note that results will be inserted from the generated experiment CSVs.

## 9. Alpha Sensitivity
- Explain how the alpha grid changes the fused result.
- Describe the intended plot for this section.
- Note which cases are stable or sensitive to weighting.

## 10. Human Evaluation Plan
- Explain the empathy, social presence, and trust scales.
- Describe who rates the outputs and how the template is used.
- State how this compares the three modality settings.

## 11. Case Studies
- Describe how congruent, dissonant, and ambiguous cases are selected.
- State where the case-study table will be shown.
- Explain how the examples support the report narrative.

## 12. Results and Discussion
- Summarize patterns from the generated CSVs and plots.
- Explain when fusion helps and when it does not.
- Add the key interpretation of the case-study examples.

## 13. Limitations
- Name the current technical limitations clearly.
- State the evaluation limitations and scope.
- Explain what the prototype does not claim.

## 14. Future Work
- List the next modeling upgrades.
- List the next evaluation upgrades.
- Mention future improvements to calibration and interaction.

## 15. Conclusion
- Restate the main contribution.
- Explain the value of the prototype as a research scaffold.
- End with the clearest take-away for the course project.

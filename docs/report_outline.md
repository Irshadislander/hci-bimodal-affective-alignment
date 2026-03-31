# Report Outline

## Title
- Confirm the final paper title and subtitle.
- Frame the project as a research prototype in HCI.
- Keep the title aligned with the report draft and presentation.

## Abstract
- State the problem, the bimodal approach, and the evaluation workflow.
- Mention text emotion, face emotion, fusion, and empathetic response generation.
- Note that the paper is backed by generated CSVs, plots, and case studies.

## 1. Introduction and Motivation
- Why does emotion-aware interaction matter in HCI?
- Why are text and facial cues useful together?
- What makes this project a meaningful course-project prototype?

## 2. Research Question
- Write the main question in one sentence.
- Add the alpha-sensitivity subquestion.
- Explain why the question fits a focused course project.

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
- What dimensions should raters score and why?
- How will the empathy, social presence, trust, and helpfulness scales be described?
- Who are the raters, and what instructions will they receive?
- How will text-only, face-only, and fused outputs be compared?
- Which CSV template collects the ratings?
- What will the report say if completed ratings are available or unavailable?

## 11. Case Studies
- How are congruent, dissonant, and ambiguous cases selected?
- Which examples best illustrate multimodal alignment?
- What should the case-study table communicate about the system?
- Which response patterns are worth highlighting in the write-up?
- How do the case studies support the report narrative?

## 12. Results and Discussion
- What patterns appear in the ablation and alpha-sensitivity outputs?
- When does fusion improve over the unimodal baselines?
- Where do the modalities disagree, and what does that reveal?
- What do the case studies suggest about the response generator?
- How should the team interpret mixed or weak results?

## 13. Limitations
- What is still simulated or fallback-based?
- What are the evaluation and data-collection limitations?
- What kinds of errors or bias remain?
- What is clearly out of scope for this prototype?

## 14. Future Work
- What is the next model enhancement for text or face analysis?
- What is the next interaction enhancement for the demo?
- How could the evaluation be strengthened?
- What additional modalities or datasets would be useful?

## 15. Conclusion
- What is the single strongest takeaway?
- How does the project serve as a research scaffold?
- Why is this a meaningful HCI prototype?
- What final sentence should close the paper?

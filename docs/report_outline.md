# HCI Bimodal Affective Alignment

## Title
- Working title: HCI Bimodal Affective Alignment
- Optional subtitle: A mini research prototype for multimodal emotion-aware interaction

## Abstract
- One-paragraph summary of the problem, method, prototype design, and early findings
- Mention text emotion recognition, facial emotion simulation, weighted fusion, and response generation

## Introduction
- Motivation for emotion-aware interaction in HCI
- Why combining textual and facial affect can improve system responsiveness
- Scope of the prototype and what is intentionally left for later work

## Research Question
- Primary question: Can simple multimodal affect fusion improve perceived empathy in a prototype interaction?
- Secondary question: How does weighting text versus face affect the fused prediction?

## Related Work
- Emotion recognition from text
- Facial affect recognition in HCI
- Multimodal fusion strategies
- Empathetic response generation systems

## Methodology
- Describe the rule-based text detector
- Describe the simulated facial emotion module
- Describe the weighted fusion scheme
- Describe the response generator and demo workflow

## System Architecture
- Input: user text and simulated facial signal
- Processing: emotion scoring, probability normalization, fusion
- Output: top emotion and short empathetic response

## Fusion Equation
- `Fused(e) = alpha * Text(e) + (1 - alpha) * Face(e)`
- `Top emotion = argmax_e Fused(e)`
- Discuss the interpretation of `alpha`

## Experiments
- Qualitative demo runs across several example inputs
- Alpha sensitivity checks
- Comparison of text-only, face-only, and fused outputs

## Ablation Study
- Compare text-only, face-only, and bimodal fusion outputs on the same case set
- Report when fusion improves the top emotion versus when it does not
- Use alpha values `1.0`, `0.0`, and `0.5` to frame the ablation discussion
- Include a short table or figure with representative case-level predictions
- State what the ablation does and does not prove about the prototype

## Alpha Sensitivity
- Describe the alpha grid used in the prototype evaluation
- Explain how changing alpha shifts the fused emotion toward text or face signals
- Summarize stable cases versus sensitive cases
- Report whether certain emotions are dominated by one modality
- Include one plot or compact table showing the alpha trend

## Case Studies
- Which 2 to 4 cases best represent congruent, dissonant, and ambiguous signals?
- For each case, what are the text, face, fused, and response outputs?
- Why is the chosen case interesting for the paper or slide deck?
- Does the fused emotion match the intended interpretation of the case?
- What makes the response feel supportive or mismatched in that example?
- How do these examples help the reader understand the research question?

## Human Evaluation Plan
- Who will review the outputs, and what is the expected participant profile?
- What task will participants perform when rating a case?
- How will empathy, social presence, and trust be scored on the 1-5 scale?
- How many cases will each participant see, and in what order?
- Will the evaluation compare text-only, face-only, and fused outputs side by side?
- What consent, privacy, and anonymity notes are needed for a course project setting?

## Results and Discussion
- What patterns appear across the ablation and alpha-sensitivity tables?
- When does text dominate the fused result, and when does face dominate?
- Which cases look most stable across alpha values?
- Which cases are sensitive to small changes in alpha, and why?
- What do the case studies reveal about congruent versus dissonant signals?
- What behavior should be highlighted as a strength of the prototype versus a limitation?

## Limitations
- Which parts of the system are still simulated or approximate?
- Where can the transformer or face pipeline fail in practice?
- What kinds of emotion or context are still hard for the prototype?
- How do missing faces, ambiguous text, or conflicting signals affect results?
- Why do these limitations matter for interpreting the evaluation results?

## Future Work
- Replace text heuristics with a trained model
- Replace the simulated face module with webcam inference
- Add calibration and confidence visualization
- Run a larger human evaluation

## Conclusion
- What is the main takeaway from the prototype evaluation?
- How did the fusion strategy help, and where did it not help?
- What does the case-study workflow show about congruent versus dissonant signals?
- How should readers interpret the project as a research scaffold rather than a finished system?

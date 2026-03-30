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
- Select 2 to 4 interesting examples that show clear success or failure modes
- Show the input text, text prediction, face prediction, fused prediction, and response
- Explain why the fused decision makes sense, or where it is surprising
- Use these examples to make the system behavior concrete for the reader
- Tie the examples back to the research question

## Human Evaluation Plan
- Describe the planned participant task or informal review process
- State what participants will rate: empathy, clarity, and emotional alignment
- Explain how the evaluation will compare text-only, face-only, and fused outputs
- Note the expected sample size and any ethics or consent considerations
- Clarify that this is a prototype-level evaluation, not a clinical study

## Results and Discussion
- Summarize patterns observed in the demo outputs
- Explain when the fusion behaves well
- Note cases where the rule-based heuristic is limited
- Include the ablation and alpha-sensitivity findings
- Discuss the strongest case-study examples and why they matter

## Limitations
- Text module is rule-based, not learned
- Facial emotion is simulated rather than captured from a camera
- Response generation is template-based
- Small prototype scale limits generalization

## Future Work
- Replace text heuristics with a trained model
- Replace the simulated face module with webcam inference
- Add calibration and confidence visualization
- Run a larger human evaluation

## Conclusion
- Restate the research goal and the value of bimodal affective alignment
- Emphasize that the prototype is a research scaffold, not a final system

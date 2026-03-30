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
- Text only
- Face only
- Weighted fusion
- Response generation without fusion context

## Human Evaluation
- Small user study or informal feedback session
- Perceived empathy
- Perceived correctness of emotion detection
- Perceived usefulness of the response

## Results and Discussion
- Summarize patterns observed in the demo outputs
- Explain when the fusion behaves well
- Note cases where the rule-based heuristic is limited

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

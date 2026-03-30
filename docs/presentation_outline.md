# Presentation Outline

## 1. Title
- HCI Bimodal Affective Alignment
- Presenter, course, and date

## 2. Motivation
- Why emotion-aware HCI matters
- Why empathy and alignment matter in interactive systems

## 3. Problem Statement
- Single-modal emotion signals can be unreliable
- Need a simple prototype that fuses text and facial cues

## 4. Research Question
- Can a lightweight bimodal pipeline improve the quality of emotion-aware responses?

## 5. Proposed System
- Text emotion module
- Facial emotion module
- Weighted fusion
- Empathetic response generation

## 6. Text Emotion Module
- Rule-based keyword scoring
- Probability normalization

## 7. Facial Emotion Module
- Simulated facial probability profiles
- Prototype-ready placeholder for later vision integration

## 8. Fusion Strategy
- Weighted average with alpha
- Top emotion selection

## 9. Response Generation
- Emotion-conditioned template responses
- Short, supportive, safe output

## 10. Demo Flow
- Enter text
- Set alpha
- Run analysis
- Review text, face, fused, and final outputs

## 11. Ablation Study
- Show the side-by-side comparison for text-only, face-only, and fused modes
- Highlight at least one case where fusion changes the final interpretation
- Mention the alpha values used for the study
- Explain why this slide matters for the research question

## 12. Alpha Sensitivity
- Show how alpha moves the fused prediction toward text or face
- Point out stable cases versus sensitive cases
- Mention the default alpha choices used in the prototype
- Explain how this informs weighting decisions

## 13. Case Study
- Walk through one representative example end-to-end
- Show the input text, image signal, fused output, and response
- Briefly explain why the response is appropriate
- Use this slide to make the prototype feel concrete

## 14. Results
- Example outputs from the evaluation workflow
- Observed effect of alpha changes
- Key ablation findings
- Short summary of the strongest case-study examples
- Brief note on the current limitations and the human-evaluation plan

## 15. Conclusion
- Main takeaway
- Why the prototype is a useful research scaffold
- What the next iteration should improve

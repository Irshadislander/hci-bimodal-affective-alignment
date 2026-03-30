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

## 13. Human Evaluation
- Explain the 1-5 rating scheme for empathy, social presence, and trust
- Show the human-evaluation template and how reviewers will use it
- Describe how the template supports a small course-project study
- Mention what reviewers should look for when comparing modalities

## 14. Case Study Examples
- Walk through one congruent case, one dissonant case, and one ambiguous case
- Show the input text, image signal, fused output, and response
- Explain why each case is interesting for the report
- Use this slide to make the prototype behavior concrete
- Point out which examples are strongest for the final paper

## 15. Results Discussion
- Summarize the ablation outputs and what they show about fusion
- Show the alpha-sensitivity trend and describe the key takeaway
- Explain how the case studies support or challenge the main claim
- Mention the human-evaluation workflow as the next step for validation
- Note the main limitations that remain in the current prototype

## 16. Final Conclusion
- State the main takeaway in one sentence
- Reiterate why bimodal affective alignment is useful in HCI
- Explain why this prototype is a research scaffold, not a finished product
- End with the clearest next step for the project

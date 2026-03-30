# Final Presentation Draft

## 1. Title
- HCI Bimodal Affective Alignment
- Text emotion, face emotion, weighted fusion, and empathetic response generation
- Day 8 final prototype for the course project

Speaker notes:
- Introduce the project as a small but serious research-style HCI prototype.
- State that the system compares text-only, face-only, and fused affective signals.
- Preview that the demo includes evaluation tools, case studies, and report assets.

## 2. Motivation
- Emotion-aware interaction is a core HCI problem.
- Single-modality emotion signals are often incomplete or unstable.
- The project explores whether a simple bimodal baseline is more informative.

Speaker notes:
- Explain that the goal is not a production system, but a strong research scaffold.
- Emphasize that user emotion is often visible in both language and facial cues.
- Motivate the need for a lightweight prototype that the class can actually evaluate.

## 3. Problem Statement
- Text alone can miss nonverbal cues.
- Facial cues alone can miss linguistic context.
- A small weighted fusion layer provides a practical comparison point.

Speaker notes:
- Frame the problem as alignment between what the user says and how the face appears.
- Point out that the system must still be stable and demo-friendly.
- Mention that the project keeps the seven-emotion schema throughout the pipeline.

## 4. Research Question
- Can a simple bimodal affective system produce more aligned emotion estimates than either modality alone?
- How sensitive is the final output to the text-face weighting parameter alpha?

Speaker notes:
- State the main question in one sentence, then immediately connect it to alpha sensitivity.
- Clarify that the comparison is text-only vs face-only vs fused.
- Keep the question grounded in the project’s actual implementation.

## 5. System Architecture
- Input: user text plus uploaded facial image.
- Processing: text emotion, face emotion, weighted fusion, and response generation.
- Output: detected emotion plus a short empathetic response.

Speaker notes:
- Walk through the pipeline from left to right.
- Mention that the Streamlit app is the main interface for the prototype.
- Point out that CSVs and plots are saved under `experiments/` for report writing.

## 6. Text Emotion Module
- Uses a pretrained transformer-based classifier when available.
- Falls back to a deterministic rule-based detector when needed.
- Outputs probabilities over seven emotions.

Speaker notes:
- Explain that the text path is transformer-first but safe to run offline.
- Mention the seven emotion labels and the normalization step.
- Keep this slide short and focused on robustness.

## 7. Face Emotion Module
- Uses image-based facial emotion analysis.
- Falls back to a safe neutral distribution if analysis fails.
- Outputs probabilities over the same seven emotions.

Speaker notes:
- Clarify that the Day 8 prototype uses uploaded images, not webcam capture.
- Mention the graceful fallback path so the demo does not break if a face is not detected.
- Keep the emphasis on stable evaluation rather than model complexity.

## 8. Fusion Strategy
- Weighted fusion combines text and face probabilities.
- Alpha controls the balance between the two modalities.
- Fused emotion is the top label from the combined distribution.

Speaker notes:
- Present alpha as the central experimental parameter.
- Mention the comparison modes: alpha 1.0 for text-only, alpha 0.0 for face-only, and alpha 0.5 for the bimodal setting.
- Tie the fusion equation directly to the evaluation workflow.

## 9. Response Generation
- Generates a short empathetic response from the fused emotion.
- Keeps the output supportive, safe, and demo-appropriate.
- Uses the final emotion rather than the raw modality outputs.

Speaker notes:
- Explain that the response layer is intentionally simple so the project stays readable.
- Point out that the system is designed to feel human-centered, not automated in a cold way.
- Remind the audience that the response is a demonstration artifact, not a conversational agent.

## 10. Ablation Study
- Compare text-only, face-only, and fused outputs on a fixed case set.
- Use the generated ablation CSV and summary plot.
- Identify where fusion changes the detected emotion or improves alignment.

Speaker notes:
- Show `experiments/ablation_counts.png` on this slide.
- Walk through one or two cases where the unimodal signals differ.
- Explain why this slide matters for the research narrative.

## 11. Alpha Sensitivity
- Sweep alpha across a small grid of values.
- Observe how the fused emotion changes as text weight increases or decreases.
- Identify stable and sensitive cases.

Speaker notes:
- Show `experiments/alpha_sensitivity_plot.png` on this slide.
- Explain that alpha = 1.0 is text-only, alpha = 0.0 is face-only, and alpha = 0.5 is the default fused setting.
- Mention any cases where the top emotion stays stable across the grid.

## 12. Human Evaluation
- Present the rating sheet for empathy, social presence, trust, and helpfulness.
- Compare the three modes using a 1-5 scale.
- Summarize the current averages if completed ratings are available.

Speaker notes:
- Show the human rating sheet and, if available, the aggregated summary plot.
- Explain that the team should collect ratings from 4-8 people for a small but useful study.
- If the completed ratings are not available yet, say that the template is ready and the summary will be filled from the CSV.

## 13. Case Studies
- Show representative congruent, dissonant, and ambiguous examples.
- Use the case-study table to illustrate system behavior.
- Highlight how the response changes across modes.

Speaker notes:
- Show `experiments/case_studies.csv` or a compact table derived from it.
- Walk the audience through one congruent example, one dissonant example, and one ambiguous example.
- Explain how these examples support the discussion of multimodal alignment.

## 14. Limitations and Future Work
- The face path is still prototype-level and image-based only.
- Human evaluation may be small and course-project scoped.
- Future work should improve robustness, calibration, and broader evaluation.

Speaker notes:
- Be direct about what the system does not claim.
- Mention the main upgrade path: stronger models, better calibration, and richer interaction.
- End this slide by showing that the project is intentionally designed as a research scaffold.

## 15. Conclusion
- The prototype demonstrates a full bimodal affective pipeline.
- The evaluation workflow supports report writing and presentation preparation.
- The project offers a practical baseline for future HCI work.

Speaker notes:
- Restate the main contribution in one sentence.
- Close by connecting the project to multimodal affective alignment in HCI.
- Leave the audience with the idea that the system is useful as both a demo and a research prototype.

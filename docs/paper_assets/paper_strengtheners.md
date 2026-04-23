# Paper Strengtheners

## Contributions Draft
- We implement an end-to-end bimodal affective alignment prototype that combines text emotion inference, face emotion inference, weighted fusion, and empathetic response generation in a reproducible pipeline.
- We provide a complete classroom evaluation toolkit: ablation outputs, alpha-sensitivity sweeps, mode-comparison cases, and a human-rating workflow with aggregation and plotting utilities.
- We contribute report-ready artifacts (tables, plots, and LaTeX blocks) that make the project auditable and easy to present in an IEEE-style format.

## Limitations and Future Work Draft
- The current face-emotion pathway is constrained by simplified profile behavior and should be upgraded with stronger vision models for broader realism.
- Human evaluation is currently preliminary (pilot with one completed rater, R1), so claims must remain conservative.
- Response generation is template-based for reproducibility; future work should test richer generation while preserving controllability.
- The case set is limited in size and scope; future iterations should expand domain coverage and participant diversity.

## Threats to Validity / Evaluation Limitations
- Small sample size in human ratings limits statistical reliability and generalizability.
- Classroom case prompts may not reflect all real-world multimodal contexts.
- The alpha sweep assesses sensitivity, but does not by itself establish external performance guarantees.

## Reproducibility Note
- All core outputs are generated from repository scripts and CSV artifacts in `experiments/`.
- The evaluation and aggregation pipeline is implemented in `app/final_evaluation_pack.py` and plotting utilities in `app/plot_results.py`.
- Generated paper assets in `docs/paper_assets/` can be regenerated directly from existing project data.

## System Robustness Note
- The fusion stage combines normalized probability vectors, which helps avoid abrupt failures when one modality is weak or noisy.
- The pipeline can still return a stable fused emotion and response for ambiguous inputs by relying on available modality signal and deterministic fallback behavior.
- This robustness should be interpreted as practical stability for a classroom prototype, not as production-grade fault tolerance.

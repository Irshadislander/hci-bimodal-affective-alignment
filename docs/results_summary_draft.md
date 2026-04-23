# Results Summary Draft

## Key Technical Achievements
The project now includes a full bimodal affective pipeline: text emotion recognition, image-based facial emotion analysis, weighted fusion, and empathetic response generation. The implementation is structured as a research prototype rather than a production system, which makes it easier to explain, test, and extend. The evaluation layer adds ablation studies, alpha sensitivity sweeps, human-evaluation templates, case studies, and report-ready assets.

## Ablation Results Placeholders
The ablation study compares text-only, face-only, and fused behavior on the default case set. The final report should insert the generated counts table or summary plot here. If the fused mode changes the top emotion in the more ambiguous or dissonant cases, that pattern should be called out explicitly. If the results remain similar across modes, that should also be interpreted carefully as a sign that the prototype may be conservative.

## Alpha Sensitivity Placeholders
The alpha-sensitivity sweep is intended to show how sensitive the system is to the balance between text and face probabilities. The final report should insert the plot generated from `experiments/alpha_sensitivity.csv`. Discussion should focus on which cases are stable across the alpha grid and which cases shift when the text or face signal is weighted more heavily.

## Human Evaluation (Pilot)
Preliminary human evaluation (pilot) with one completed rater (R1).

This is an initial classroom evaluation with one completed rating sheet (30 rows total, 10 per mode). Early averages in `experiments/human_eval_summary.csv` are strongest for fused mode and lower for face-only mode, but this should be treated as a first-pass signal rather than a general conclusion until more raters are added.

## Case Study Highlights
The case studies intentionally mix congruent, dissonant, and ambiguous examples so the report can show different kinds of multimodal alignment. The final write-up should highlight cases where text and face agree, cases where they conflict, and cases where the fused output resolves the tension in a reasonable way. A compact table or a few short examples should be enough to support the narrative.

## What Remains Before Final Submission
The remaining work is mostly editorial and evaluative: add more human raters beyond R1, finalize the report tables and plots, polish the presentation slides, and proofread the final draft for consistency. The current human-evaluation results should be presented explicitly as preliminary pilot evidence.

# Results Summary Draft

## Key Technical Achievements
The project now contains a full bimodal affective pipeline: text emotion recognition, image-based facial emotion analysis, weighted fusion, and empathetic response generation. The implementation is structured as a mini research prototype rather than a production system, which makes it easier to explain, test, and extend. The evaluation layer adds ablation studies, alpha sensitivity sweeps, human-evaluation templates, case studies, and report-ready assets.

## Ablation Results Placeholders
The ablation study compares text-only, face-only, and fused behavior on the default case set. The final report should insert the generated counts table or summary plot here. If the fused mode changes the top emotion in the more ambiguous or dissonant cases, that pattern should be called out explicitly. If the results remain similar across modes, that should also be interpreted carefully as a sign that the prototype may be conservative.

## Alpha Sensitivity Placeholders
The alpha-sensitivity sweep is intended to show how sensitive the system is to the balance between text and face probabilities. The final report should insert the plot generated from `experiments/alpha_sensitivity.csv`. Discussion should focus on which cases are stable across the alpha grid and which cases shift when the text or face signal is weighted more heavily.

## Human Evaluation Placeholders
Human evaluation is designed to compare empathy, social presence, trust, and helpfulness across the three modes. The report should insert averages from the completed human-rating sheet once ratings are collected. Until then, the draft should state that the template is ready and the summary table will be generated from `experiments/human_rating_sheet_completed.csv`.

## Case Study Highlights
The case studies intentionally mix congruent, dissonant, and ambiguous examples so the report can show different kinds of multimodal alignment. The final write-up should highlight cases where text and face agree, cases where they conflict, and cases where the fused output resolves the tension in a reasonable way. A compact table or a few short examples should be enough to support the narrative.

## What Remains Before Final Submission
The remaining work is mostly editorial and evaluative: collect human ratings, finalize the report tables and plots, polish the presentation slides, and proofread the final draft for consistency. If any completed ratings are missing, the team can still present the evaluation template and explain the intended study design clearly.

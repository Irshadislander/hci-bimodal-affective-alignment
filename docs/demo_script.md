# Demo Script

## Demo Setup Checklist
- Start the Streamlit app with `streamlit run app/main.py`.
- Keep the `experiments/` folder visible so you can point to generated CSVs and plots.
- Have one clear facial image ready, ideally a front-facing selfie with a neutral or slightly happy expression.
- Keep one short text example ready for the first run.
- If possible, have the ablation and human-evaluation outputs pre-generated before class.

## Live Demo Flow
1. Open the app and briefly state the project goal.
2. Type a short message into the text box.
3. Upload the facial image.
4. Run the analysis and walk through the text, face, fused, and response sections.
5. Change alpha to show how the fused output responds to different weights.
6. Show the evaluation tools and final human-evaluation pack.

## What Text to Type
- Primary demo text: `I am okay, but a little tired.`
- Congruent text example: `I am thrilled with the result and feel genuinely happy.`
- Dissonant text example: `I am thrilled with the result, but the room felt gloomy to me.`

## What Image to Upload
- Use a clear frontal face photo with even lighting.
- A neutral expression works well for showing the face fallback and comparison behavior.
- A slight smile is also fine if you want the face signal to lean more positive.

## What Outputs to Point Out
- The text emotion probability table.
- The face emotion probability table.
- The fused emotion table and the top 3 fused emotions.
- The final detected emotion callout.
- The short empathetic response.

## When to Show Ablation Study
- Show the ablation study after the first live analysis.
- Explain that it compares text-only, face-only, and fused settings.
- Point out how the fused mode differs from the unimodal baselines.

## When to Show Human Evaluation Sheet
- Show the human rating sheet after the ablation discussion.
- Explain that raters use empathy, social presence, trust, and helpfulness on a 1-5 scale.
- Mention that the completed sheet can be aggregated to produce report-ready summary tables and plots.

## Fallback Plan if Live Demo Fails
- If image upload fails, continue with the text-only path and explain the face fallback.
- If the transformer model is unavailable, note that the rule-based fallback is already built in.
- If the app itself cannot be shown, open the generated CSVs and plots in `experiments/`.
- End by showing the final report draft and case-study table so the narrative still lands.

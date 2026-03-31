# Demo Script

## Demo Setup Checklist
- Start the app with `streamlit run app/main.py`.
- Make sure the `experiments/` folder is visible in your file browser.
- Keep a clean frontal face image ready in `.png` or `.jpg` format.
- Have the report draft, presentation draft, and submission checklist open in separate tabs.
- Keep screenshots of the ablation plot, alpha plot, case studies, and human-evaluation sheet ready in case the live demo needs a backup.

## Exact Demo Order
1. Open the app and state the project title.
2. Explain that the system combines text emotion, face emotion, weighted fusion, and empathetic response generation.
3. Run the first analysis with no image uploaded.
4. Run a second analysis with an uploaded face image.
5. Change alpha to `1.0`, `0.5`, and `0.0` to show the baseline and fused behaviors.
6. Open the evaluation tools and show the ablation and alpha-sensitivity outputs.
7. Open the final human-evaluation pack and show the mode comparison cases and rating sheet.
8. End with the report draft, presentation draft, and submission checklist.

## Exact Text Inputs
- Neutral / fallback demo: `I am okay, but a little tired.`
- Positive demo: `I am thrilled with the result and feel genuinely happy.`
- Dissonant demo: `I am thrilled with the result, but the room felt gloomy to me.`
- Negative demo: `I am angry about the delay, and it has been frustrating all day.`

## Exact Image Usage
- For the first live pass, do not upload an image so the face fallback path is visible.
- For the second live pass, upload the prepared face image before clicking `Run Analysis`.
- If the face image is neutral, point out that the face distribution remains mostly neutral.
- If the face image is expressive, point out how the face probabilities influence the fused result.

## What to Point Out During the Demo
- The text emotion probability table and the backend status message.
- The face emotion probability table and the fallback warning when no image is supplied.
- The fused emotion table and the top 3 fused emotions.
- The final detected emotion and the short empathetic response.
- The ablation table and alpha-sensitivity results.
- The mode comparison cases and the human rating sheet.
- The report tables and report status docs if you generated them ahead of time.

## What Backup Screenshots to Keep Ready
- The home screen of the Streamlit app.
- A screenshot of the text-only analysis output.
- A screenshot of the face analysis output with an uploaded image.
- A screenshot of the ablation results table or plot.
- A screenshot of the alpha-sensitivity plot.
- A screenshot of the mode comparison cases table.
- A screenshot of the human rating sheet.
- A screenshot of the final report draft or presentation draft.

## Fallback Plan if the Live Demo Fails
- If the image analysis fails, explain that the prototype already includes a safe neutral fallback.
- If the transformer model is unavailable, explain that the text module falls back to a rule-based detector.
- If Streamlit cannot launch, open the generated CSVs and markdown files directly.
- If time is limited, show the case studies and the final report draft first, then summarize the pipeline verbally.

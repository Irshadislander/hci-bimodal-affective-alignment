# HCI Bimodal Affective Alignment

This project is a mini research-style Human-Computer Interaction system that combines:
- pretrained transformer-based text emotion recognition when available
- facial emotion recognition
- weighted emotion fusion
- empathetic response generation

## Project Goal
To build a bimodal affective alignment system that improves emotional understanding in human-computer interaction.

## Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run
./run.sh

## Facial Input
- Upload a face image in the Streamlit app to run image-based facial emotion analysis.
- If no image is uploaded, the app uses a safe neutral fallback distribution for the face signal.

## Text Emotion
- The app uses a pretrained HuggingFace text emotion model when available.
- If model loading fails, it falls back to the rule-based detector automatically.

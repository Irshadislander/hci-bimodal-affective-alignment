"""Short empathetic response generation for the demo."""

from __future__ import annotations

import random

_RESPONSES = {
    "happy": [
        "That sounds positive. I am glad it is going well.",
        "Nice, that reads as a good moment.",
        "That feels upbeat and encouraging.",
        "I am picking up a positive tone here.",
    ],
    "sad": [
        "I am sorry this feels hard. We can take it step by step.",
        "That sounds heavy. I am here to help make it easier.",
        "I hear some sadness. We can keep moving gently.",
        "That seems difficult. Let us focus on one small next step.",
    ],
    "angry": [
        "I can see frustration here. Let us slow it down.",
        "That sounds tense. We can work through it carefully.",
        "I hear the frustration. I will keep this calm and direct.",
        "That feels heated. We can make the next step more manageable.",
    ],
    "neutral": [
        "Thanks for sharing. I will keep this clear and concise.",
        "That seems steady. I can help with the next step.",
        "Understood. I will stay focused and supportive.",
        "I am getting a neutral signal, so I will keep this practical.",
    ],
    "fear": [
        "That sounds uncertain. I can help make the next step feel safer.",
        "I hear some worry. Let us make this feel more manageable.",
        "That seems a little tense. We can slow down and clarify it.",
        "I can help reduce uncertainty by breaking this down.",
    ],
    "surprise": [
        "That feels unexpected. I can help unpack it.",
        "Interesting. We can make sense of it together.",
        "I am seeing some surprise here, so let us look at it closely.",
        "That seems a bit sudden. I can help sort through it.",
    ],
    "disgust": [
        "That sounds unpleasant. I can help steer toward a better path.",
        "I hear discomfort there. Let us move toward something more workable.",
        "That seems off-putting. We can keep the interaction comfortable.",
        "That feels strongly negative. I can help redirect us.",
    ],
}


def generate_response(user_text: str, fused_emotion: str) -> str:
    """Generate a short empathetic response from the fused emotion."""

    emotion = (fused_emotion or "neutral").strip().lower()
    options = _RESPONSES.get(emotion, _RESPONSES["neutral"])
    return random.choice(options)

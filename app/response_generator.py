"""Short empathetic response generation for the demo."""

from __future__ import annotations

_RESPONSES = {
    "happy": "That sounds positive. I am glad the interaction feels good.",
    "sad": "I am sorry this feels heavy. We can take it one step at a time.",
    "angry": "I can see some frustration. Let us slow down and make this easier.",
    "neutral": "Thanks for sharing that. I will keep the response clear and supportive.",
    "fear": "That sounds uncertain. I can help make the next step feel more manageable.",
    "surprise": "That is an interesting reaction. I can help unpack it with you.",
    "disgust": "That sounds unpleasant. Let us steer toward a more comfortable path.",
}


def generate_response(user_text: str, fused_emotion: str) -> str:
    """Generate a short empathetic response from the fused emotion."""

    emotion = (fused_emotion or "neutral").strip().lower()
    return _RESPONSES.get(emotion, _RESPONSES["neutral"])

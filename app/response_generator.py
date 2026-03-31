"""Short empathetic response generation for the prototype."""

from __future__ import annotations

import hashlib

_RESPONSES = {
    "happy": [
        "That sounds genuinely positive. I am glad things are going well.",
        "Nice, that comes across as encouraging.",
        "I am picking up an upbeat tone here.",
        "That feels like a constructive moment.",
    ],
    "sad": [
        "I am sorry this feels difficult. We can take it one step at a time.",
        "That sounds heavy, and I appreciate you sharing it.",
        "I hear some sadness here. Let us keep this gentle.",
        "That seems hard. We can focus on one small next step.",
    ],
    "angry": [
        "I can hear the frustration. Let us keep the next step practical.",
        "That sounds tense, and I will stay concise and helpful.",
        "This reads as strongly negative. We can slow it down.",
        "That feels frustrating. Let us make it more manageable.",
    ],
    "neutral": [
        "Thanks for sharing. I will keep things straightforward and helpful.",
        "That seems steady. I can help with the next step.",
        "Understood. I will stay focused and supportive.",
        "This reads as neutral, so I will keep the response practical.",
    ],
    "fear": [
        "That sounds uncertain. Let us break it into a clear next step.",
        "I hear some worry here. We can make this feel more manageable.",
        "That seems a little tense, so we can slow down and clarify it.",
        "I can help reduce uncertainty by making the next step concrete.",
    ],
    "surprise": [
        "That feels unexpected. We can unpack it together.",
        "Interesting. Let us make sense of it calmly.",
        "I am seeing some surprise here, so we can look at it closely.",
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
    seed_source = f"{emotion}|{user_text}".encode("utf-8", errors="ignore")
    index = int(hashlib.sha256(seed_source).hexdigest(), 16) % len(options)
    return options[index]

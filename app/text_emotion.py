"""Rule-based text emotion detection for the starter demo."""

from __future__ import annotations

import re
from collections import Counter

EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]

_BASE_SCORES = {
    "happy": 0.8,
    "sad": 0.8,
    "angry": 0.7,
    "neutral": 5.0,
    "fear": 0.6,
    "surprise": 0.6,
    "disgust": 0.5,
}

_EMOTION_KEYWORDS = {
    "happy": {"happy", "excited", "great", "awesome", "glad", "joy", "joyful", "love", "wonderful"},
    "sad": {"sad", "upset", "down", "blue", "tired", "lonely", "depressed", "bad"},
    "angry": {"angry", "mad", "frustrated", "annoyed", "furious", "irritated"},
    "fear": {"worried", "anxious", "scared", "nervous", "afraid", "uncertain"},
    "surprise": {"surprised", "shocked", "wow", "unexpected", "amazed"},
    "disgust": {"disgusted", "gross", "nasty", "ew", "repulsed"},
}

_NEUTRALISH_WORDS = {"fine", "okay", "ok"}
_MAJOR_BOOST = 10.0
_NEUTRAL_BOOST = 5.0
_SADNESS_BOOST_FOR_NEUTRALISH = 1.5


def _tokenize(text: str) -> Counter[str]:
    """Return a simple word counter for lowercase word tokens."""

    return Counter(re.findall(r"[a-z']+", text.lower()))


def _normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    """Normalize a raw score dictionary into a probability distribution."""

    total = sum(scores.values())
    if total <= 0:
        return {emotion: 1.0 / len(EMOTIONS) for emotion in EMOTIONS}
    return {emotion: scores[emotion] / total for emotion in EMOTIONS}


def detect_text_emotion(text: str) -> dict[str, float]:
    """Estimate emotion probabilities from text using simple rules.

    The output always contains the seven starter emotions and sums to 1.0
    after normalization.
    """

    tokens = _tokenize(text or "")
    scores = dict(_BASE_SCORES)

    if any(token in _NEUTRALISH_WORDS for token in tokens):
        scores["neutral"] += _NEUTRAL_BOOST
        scores["sad"] += _SADNESS_BOOST_FOR_NEUTRALISH

    for emotion, keywords in _EMOTION_KEYWORDS.items():
        hits = sum(count for word, count in tokens.items() if word in keywords)
        if hits:
            scores[emotion] += _MAJOR_BOOST * hits

    return _normalize_scores(scores)

"""Rule-based text emotion detection for the Day 2 prototype."""

from __future__ import annotations

import re

EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]

_KEYWORD_BANKS = {
    "happy": {
        "happy": 2.2,
        "excited": 2.0,
        "great": 1.8,
        "awesome": 2.0,
        "good": 1.0,
        "glad": 1.5,
        "pleased": 1.4,
        "proud": 1.3,
        "relieved": 1.2,
        "joy": 1.8,
        "wonderful": 2.1,
        "love it": 1.7,
        "feeling good": 1.6,
    },
    "sad": {
        "sad": 2.2,
        "upset": 1.8,
        "down": 1.3,
        "tired": 1.1,
        "lonely": 1.7,
        "hurt": 1.5,
        "blue": 1.2,
        "disappointed": 1.8,
        "discouraged": 1.5,
        "not okay": 2.0,
        "not good": 1.8,
        "feeling low": 1.6,
        "rough day": 1.4,
    },
    "angry": {
        "angry": 2.3,
        "mad": 2.0,
        "frustrated": 2.1,
        "annoyed": 1.5,
        "furious": 2.3,
        "irritated": 1.7,
        "fed up": 1.9,
        "bothered": 1.2,
        "rage": 2.2,
        "resentful": 1.5,
        "stressed": 1.1,
    },
    "neutral": {
        "okay": 1.8,
        "ok": 1.8,
        "fine": 1.7,
        "alright": 1.5,
        "steady": 1.1,
        "calm": 1.0,
        "normal": 1.0,
        "manageable": 1.0,
        "mixed": 0.9,
        "so so": 1.3,
        "just checking": 1.0,
        "for now": 0.8,
    },
    "fear": {
        "worried": 2.1,
        "anxious": 2.2,
        "scared": 2.1,
        "nervous": 1.9,
        "afraid": 2.2,
        "uncertain": 1.7,
        "uneasy": 1.6,
        "tense": 1.3,
        "overwhelmed": 1.8,
        "not sure": 1.7,
        "concerned": 1.5,
    },
    "surprise": {
        "surprised": 2.1,
        "shocked": 2.2,
        "wow": 1.4,
        "unexpected": 1.9,
        "amazed": 1.8,
        "astonished": 2.0,
        "suddenly": 1.0,
        "didn't expect": 1.8,
        "unbelievable": 1.9,
        "taken aback": 1.7,
    },
    "disgust": {
        "disgusted": 2.3,
        "gross": 1.9,
        "nasty": 1.8,
        "ew": 1.5,
        "repulsed": 2.1,
        "revolting": 2.1,
        "sickening": 2.0,
        "icky": 1.6,
        "unpleasant": 1.3,
        "grossed out": 2.0,
    },
}

_NEUTRAL_HINTS = {
    "fine",
    "okay",
    "ok",
    "alright",
    "mixed",
    "so so",
    "just checking",
    "for now",
}


def normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    """Normalize raw emotion scores into a probability distribution."""

    cleaned = {
        emotion: max(0.0, float(scores.get(emotion, 0.0)))
        for emotion in EMOTIONS
    }
    total = sum(cleaned.values())
    if total <= 0:
        return {emotion: 1.0 / len(EMOTIONS) for emotion in EMOTIONS}
    return {emotion: cleaned[emotion] / total for emotion in EMOTIONS}


def _count_term(term: str, text_lower: str) -> int:
    """Count exact term matches in the normalized text string."""

    pattern = rf"\b{re.escape(term)}\b"
    return len(re.findall(pattern, text_lower))


def detect_text_emotion(text: str) -> dict[str, float]:
    """Estimate emotion probabilities from text using lexical heuristics.

    Multiple keyword matches raise the associated emotion score, while neutral
    cues keep mixed or ambiguous text anchored toward neutral.
    """

    normalized_text = " ".join(re.findall(r"[a-z']+", (text or "").lower()))
    scores = {emotion: 0.4 for emotion in EMOTIONS}
    scores["neutral"] = 1.0

    matched_any = False

    for emotion, keyword_bank in _KEYWORD_BANKS.items():
        for term, weight in keyword_bank.items():
            hits = _count_term(term, normalized_text)
            if hits:
                matched_any = True
                scores[emotion] += weight * hits

    neutral_hits = sum(_count_term(term, normalized_text) for term in _NEUTRAL_HINTS)
    if neutral_hits:
        matched_any = True
        scores["neutral"] += 1.4 * neutral_hits
        scores["sad"] += 0.3 * neutral_hits

    if matched_any:
        scores["neutral"] += 0.5
    else:
        scores["neutral"] += 5.0

    return normalize_scores(scores)

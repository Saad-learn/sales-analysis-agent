import re
from .utils import normalize

def extract_timeline(text: str) -> dict:
    text = normalize(text)
    urgent = ["asap", "urgent", "immediately", "today", "now", "yesterday"]
    short_term = ["tomorrow", "this week", "few days", "next week", "soon"]
    long_term = ["next month", "quarter", "later", "future", "next year"]
    
    for word in urgent:
        if word in text:
            return {
                "value": "immediate",
                "score": 0.95,
                "reason": f"Urgent timeline: '{word}'"
            }

    for word in short_term:
        if word in text:
            return {
                "value": "short_term",
                "score": 0.7,
                "reason": f"Short-term timeline: '{word}'"
            }

    for word in long_term:
        if word in text:
            return {
                "value": "long_term",
                "score": 0.5,
                "reason": f"Long-term timeline: '{word}'"
            }

    if re.search(r"in \d+ (day|week|month)", text):
        return {
            "value": "short_term",
            "score": 0.75,
            "reason": "Relative time expression detected"
        }

    return {
        "value": None,
        "score": 0.2,
        "reason": "No timeline mentioned"
    }
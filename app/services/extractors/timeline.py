import re
from .utils import normalize

def extract_timeline(text: str) -> dict:
    text = normalize(text)
    urgent = ["asap", "urgent", "immediately", "today", "now"]
    short_term = ["tomorrow", "this week", "few days", "next week"]
    long_term = ["next month", "quarter", "later", "future"]
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
                "value": "short",
                "score": 0.7,
                "reason": f"Short-term timeline: '{word}'"
            }

    for word in long_term:
        if word in text:
            return {
                "value": "long",
                "score": 0.6,
                "reason": f"Long-term timeline: '{word}'"
            }

    if re.search(r"in \d+ (day|days|week|weeks)", text):
        return {
            "value": "short",
            "score": 0.75,
            "reason": "Relative time expression detected"
        }

    return {
        "value": None,
        "score": 0.2,
        "reason": "No timeline mentioned"
    }
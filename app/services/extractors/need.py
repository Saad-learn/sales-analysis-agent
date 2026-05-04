from .utils import normalize, contains_negation

def extract_need(text: str) -> dict:
    text = normalize(text)
    strong = ["need", "require", "must", "urgent requirement"]
    medium = ["looking for", "interested in", "considering", "exploring"]
    for word in strong:
        if word in text and not contains_negation(text, word):
            return {
                "value": "high",
                "score": 0.9,
                "reason": f"Strong intent keyword: '{word}'"
            }
    for word in medium:
        if word in text:
            return {
                "value": "medium",
                "score": 0.6,
                "reason": f"Moderate intent keyword: '{word}'"
            }
    return {
        "value": "low",
        "score": 0.2,
        "reason": "No clear need detected"
    }
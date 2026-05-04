from .utils import normalize, contains_negation

def extract_authority(text: str) -> dict:
    text = normalize(text)
    roles = [
        "ceo", "founder", "owner", "director",
        "manager", "head", "lead", "decision maker"
    ]
    for role in roles:
        if role in text and not contains_negation(text, role):
            return {
                "value": "high",
                "score": 0.9,
                "reason": f"Decision-making role detected: '{role}'"
            }
    if "team" in text or "we will decide" in text:
        return {
            "value": "medium",
            "score": 0.5,
            "reason": "Collective decision context"
        }
    return {
        "value": "low",
        "score": 0.2,
        "reason": "No authority indicators"
    }
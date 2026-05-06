from .utils import normalize, contains_negation

def extract_authority(text: str) -> dict:
    text = normalize(text)
    roles = [
        "ceo", "founder", "owner", "director", "cto", "cfo",
        "manager", "head", "lead", "decision maker", "vp"
    ]
    
    for role in roles:
        if role in text and not contains_negation(text, role):
            return {
                "value": "high",
                "score": 0.9,
                "reason": f"Decision-making role detected: '{role}'"
            }
    
    collaborative_terms = ["team", "we will decide", "board", "committee"]
    for term in collaborative_terms:
        if term in text:
            return {
                "value": "medium",
                "score": 0.5,
                "reason": f"Collaborative context: '{term}'"
            }
    
    return {
        "value": "low",
        "score": 0.2,
        "reason": "No authority indicators"
    }
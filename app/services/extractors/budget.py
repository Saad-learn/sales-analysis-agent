from .utils import normalize, contains_negation, find_money

def extract_budget(text: str) -> dict:
    text = normalize(text)
    match = find_money(text)
   
    if match:
        return {
            "value": match.group(),
            "score": 0.95,
            "reason": "Explicit budget mentioned"
        }
    keywords = ["budget", "cost", "price", "pricing", "quote"]
   
    for word in keywords:
        if word in text and not contains_negation(text, word):
            return {
                "value": "mentioned",
                "score": 0.7,
                "reason": f"Budget-related keyword: '{word}'"
            }
   
    if "cheap" in text or "affordable" in text:
        return {
            "value": "low_budget",
            "score": 0.6,
            "reason": "Indicates cost sensitivity"
        }
   
    if "expensive" in text:
        return {
            "value": "concern",
            "score": 0.6,
            "reason": "Price concern detected"
        }
   
    return {
        "value": None,
        "score": 0.1,
        "reason": "No budget information found"
    }
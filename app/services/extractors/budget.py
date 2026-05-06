import re
from .utils import normalize, contains_negation, find_money

def extract_budget(text: str) -> dict:
    normalized_text = normalize(text)
    
    money_match = find_money(normalized_text)
    if money_match:
        if not contains_negation(normalized_text, money_match.group()):
            return {
                "value": money_match.group(),
                "score": 0.95,
                "reason": f"Explicit budget mentioned: '{money_match.group()}'"
            }

    shorthand_pattern = r"\b\d+\s?[km]\b"
    shorthand_match = re.search(shorthand_pattern, normalized_text)
    if shorthand_match and "budget" in normalized_text:
        return {
            "value": shorthand_match.group(),
            "score": 0.85,
            "reason": f"Shorthand budget detected: '{shorthand_match.group()}'"
        }

    keywords = ["budget", "cost", "price", "pricing", "quote", "investment"]
    for word in keywords:
        if word in normalized_text and not contains_negation(normalized_text, word):
            return {
                "value": "mentioned",
                "score": 0.7,
                "reason": f"Budget-related keyword found: '{word}'"
            }

    low_indicators = ["cheap", "affordable", "low cost", "within reach", "economical"]
    high_indicators = ["premium", "expensive", "top tier", "high end"]
    
    for word in low_indicators:
        if word in normalized_text:
            return {
                "value": "low_budget",
                "score": 0.6,
                "reason": f"Indicates cost sensitivity: '{word}'"
            }
            
    for word in high_indicators:
        if word in normalized_text:
            return {
                "value": "high_budget",
                "score": 0.6,
                "reason": f"Indicates premium interest: '{word}'"
            }

    return {
        "value": None,
        "score": 0.1,
        "reason": "No budget information found"
    }
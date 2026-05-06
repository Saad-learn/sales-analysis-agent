import re

def normalize(text: str) -> str:
    if not text:
        return ""
    return text.lower().strip()

def contains_negation(text: str, phrase: str) -> bool:
    negations = [
        f"no {phrase}", 
        f"not {phrase}", 
        f"don't {phrase}", 
        f"do not {phrase}", 
        f"can't {phrase}",
        f"cannot {phrase}",
        f"without {phrase}"
    ]
    return any(neg in text for neg in negations)

def find_money(text: str):
    pattern = r"(\$|usd|eur|pkr|rs|£|€)\s?\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s?(\$|usd|eur|pkr|rs|£|€)"
    return re.search(pattern, text, re.IGNORECASE)

import re

def normalize(text: str) -> str:
    return text.lower().strip()

def contains_negation(text: str, phrase: str) -> bool:
    return any(
        neg in text
        for neg in [
            f"no {phrase}",
            f"not {phrase}",
            f"don't {phrase}",
            f"do not {phrase}",
        ]
    )

def find_money(text: str):
    pattern = r"(\$|usd|eur|pkr|rs)\s?\d+|\d+\s?(\$|usd|eur|pkr|rs)"
    return re.search(pattern, text)
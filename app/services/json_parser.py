import json
import re

def safe_json_parse(raw: str) -> dict:
    if not raw:
        return {}

    raw = raw.strip()
    
    clean_raw = re.sub(r"^ ```json\s*|```$", "", raw, flags=re.MULTILINE).strip()

    try:
        return json.loads(clean_raw)
    except Exception:
        pass

    try:
        match = re.search(r"\{[\s\S]*\}", clean_raw)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    try:
        fixed_quotes = re.sub(r"'(.*?)'", r'"\1"', clean_raw)
        match = re.search(r"\{[\s\S]*\}", fixed_quotes)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return {}
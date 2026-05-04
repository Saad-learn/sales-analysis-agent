import json
import re
def safe_json_parse(raw: str) -> dict:
    if not raw:
        return {}
    raw = raw.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(raw)
    except Exception:
        pass
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return {}
    try:
        return json.loads(match.group())
    except Exception:
        return {}
def build_bant_prompt(email_text: str) -> str:
    return f"""
SYSTEM:
You are a strict JSON generator for B2B sales intelligence.
RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
TASK:
Analyze the email and extract BANT signals.
EMAIL:
\"\"\"{email_text}\"\"\"
OUTPUT FORMAT:
{{
  "sentiment": "positive",
  "budget": "low",
  "authority": "low",
  "need": "low",
  "timeline": "short_term",
  "score": 0.0,
  "summary": "short summary"
}}
"""
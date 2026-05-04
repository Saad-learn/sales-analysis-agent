def build_bant_prompt(email_text: str) -> str:
    return f"""
SYSTEM:
You are a strict JSON generator for B2B sales intelligence.

RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- If you fail, return: {{"error":"invalid_output"}}

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

RULES:
- sentiment: positive, neutral, negative
- budget: low, medium, high
- authority: low, medium, high
- need: low, medium, high
- timeline: immediate, short_term, long_term
- score: 0.0 - 1.0
"""
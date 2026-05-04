import json
import logging
import re

from app.services.ollama_client import OllamaClient
from app.services.prompts import build_bant_prompt

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.client = OllamaClient(model="mistral:latest")

    def _safe_parse(self, text: str):
        # 1st try: direct JSON
        try:
            return json.loads(text)
        except Exception:
            pass

        # 2nd try: regex extraction
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return None
            return json.loads(match.group(0))
        except Exception as e:
            logger.error(f"JSON parse error: {e} | RAW: {text}")
            return None

    async def analyze_email(self, email_text: str):
        try:
            prompt = build_bant_prompt(email_text[:3000])
            raw = await self.client.generate(prompt)

            logger.info(f"RAW OLLAMA RESPONSE: {raw}")

            data = self._safe_parse(raw)

            if not data or "error" in data:
                raise Exception("Invalid model output")

            return {
                "sentiment": data.get("sentiment", "neutral"),
                "budget": data.get("budget", "medium"),
                "authority": data.get("authority", "medium"),
                "need": data.get("need", "medium"),
                "timeline": data.get("timeline", "short_term"),
                "score": float(data.get("score", 0.5)),
                "summary": data.get("summary", "Generated analysis"),
            }

        except Exception as e:
            logger.error(f"AI FAILED: {e}")

            return {
                "sentiment": "neutral",
                "budget": "medium",
                "authority": "medium",
                "need": "medium",
                "timeline": "short_term",
                "score": 0.5,
                "summary": "Fallback due to model failure",
            }
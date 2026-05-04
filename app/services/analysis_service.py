import logging
import os
from app.services.ollama_client import OllamaClient
from app.services.prompts import build_bant_prompt
from app.services.json_parser import safe_json_parse

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = OllamaClient(
            model=os.getenv("OLLAMA_MODEL", "phi:latest")
        )

    async def analyze_email(self, email_text: str):
        
        if not email_text:
            return {"error": "empty_email"}
        prompt = build_bant_prompt(email_text[:3000])

        try:
            response = await self.client.generate(prompt)
            raw_output = response.get("response", "")

            if not raw_output:
                return {"error": "empty_ai_response"}
            data = safe_json_parse(raw_output)

            if not data:
                logger.error(f"Invalid JSON from model: {raw_output}")
                return {"error": "invalid_json"}
            bant = data.get("bant", {})

            def get_value(key):
                value = bant.get(key, data.get(key))
                if isinstance(value, dict):
                    return value.get("value", "Not mentioned")
                return value if value else "Not mentioned"

            return {
                "sentiment": data.get("sentiment", "neutral"),
                "budget": get_value("budget"),
                "authority": get_value("authority"),
                "need": get_value("need"),
                "timeline": get_value("timeline"),
                "score": data.get("score", 0),
                "summary": data.get("summary", "No summary provided"),
            }

        except Exception as e:
            logger.exception("AI analysis failed")
            return {"error": str(e)}
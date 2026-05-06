import os
import logging
from langchain_cerebras import ChatCerebras
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from app.services.ollama_client import OllamaClient
from app.services.prompts import build_bant_prompt
from app.services.json_parser import safe_json_parse

logger = logging.getLogger(__name__)

EMAIL_TRUNCATION_LIMIT = 3000


class BANTAnalysis(BaseModel):
    sentiment: str = Field(description="positive, neutral, or negative")
    budget: str = Field(description="low, medium, or high")
    authority: str = Field(description="low, medium, or high")
    need: str = Field(description="low, medium, or high")
    timeline: str = Field(description="immediate, short_term, or long_term")
    score: float = Field(description="A lead quality score between 0.0 and 1.0")
    summary: str = Field(description="A 1-2 sentence summary of the lead's intent")


class AIService:
    def __init__(self):
        self.parser = JsonOutputParser(pydantic_object=BANTAnalysis)
        self.ollama = OllamaClient(
            base_url=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434"),
            model=os.getenv("OLLAMA_MODEL", "phi:latest"),
        )
        self.llm = self._init_cerebras()

    def _init_cerebras(self):
        api_key = os.getenv("CEREBRAS_API_KEY")
        model = os.getenv("CEREBRAS_MODEL", "llama-3.3-70b")
        if not api_key:
            return None
        try:
            return ChatCerebras(model=model, cerebras_api_key=api_key)
        except Exception as e:
            logger.error(f"Cerebras init failed: {e}")
            return None

    async def analyze_email(self, email_text: str):
        if not email_text:
            return self._fallback("Empty input")

        truncated = email_text[:EMAIL_TRUNCATION_LIMIT]

        if self.llm:
            try:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert sales analyst. Extract BANT data.\n{format_instructions}"),
                    ("user", "Analyze: {email_content}"),
                ]).partial(format_instructions=self.parser.get_format_instructions())

                chain = prompt | self.llm | self.parser
                return await chain.ainvoke({"email_content": truncated})
            except Exception as e:
                logger.warning(f"Cerebras failed, falling back to Ollama: {e}")

        try:
            raw_output = await self.ollama.generate(build_bant_prompt(truncated))
            data = safe_json_parse(raw_output)
            if not data:
                return self._fallback("Ollama parse failed")
            return {
                "sentiment": data.get("sentiment", "neutral"),
                "budget": self._extract_val(data, "budget"),
                "authority": self._extract_val(data, "authority"),
                "need": self._extract_val(data, "need"),
                "timeline": self._extract_val(data, "timeline"),
                "score": float(data.get("score", 0.0)),
                "summary": data.get("summary", "Extracted via Local AI"),
            }
        except Exception as e:
            logger.error(f"Ollama failed: {e}")
            return self._fallback("All AI providers failed")

    def _extract_val(self, data: dict, key: str) -> str:
        val = data.get(key, "unknown")
        if isinstance(val, dict):
            return val.get("value", "unknown")
        return str(val)

    def _fallback(self, reason: str) -> dict:
        return {
            "sentiment": "neutral",
            "budget": "unknown",
            "authority": "unknown",
            "need": "unknown",
            "timeline": "unknown",
            "score": 0.0,
            "summary": reason,
        }
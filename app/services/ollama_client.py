import httpx
import asyncio


class OllamaClient:
    def __init__(self, base_url="http://127.0.0.1:11434", model="mistral:latest"):
        self.base_url = base_url.rstrip("/")
        self.model = model

        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(180.0, connect=10.0)
        )

    async def generate(self, prompt: str, retries: int = 2):
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "num_predict": 500
            }
        }

        last_error = None

        for attempt in range(retries):
            try:
                res = await self.client.post(url, json=payload)

                if res.status_code != 200:
                    raise Exception(res.text)

                data = res.json()
                text = data.get("response", "").strip()

                if not text:
                    raise Exception("Empty Ollama response")

                return text

            except Exception as e:
                last_error = str(e)
                await asyncio.sleep(1)

        raise Exception(f"Ollama failed after retries: {last_error}")
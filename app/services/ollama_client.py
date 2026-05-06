import httpx
import asyncio

class OllamaClient:
    def __init__(self, base_url="http://127.0.0.1:11434", model="mistral:latest"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(self, prompt: str, retries: int = 2):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "top_p": 0.9, "num_predict": 500}
        }
        
        last_error = None
        async with httpx.AsyncClient(timeout=httpx.Timeout(180.0)) as client:
            for attempt in range(retries):
                try:
                    res = await client.post(url, json=payload)
                    if res.status_code != 200:
                        raise Exception(f"Status {res.status_code}")
                    return res.json().get("response", "").strip()
                except Exception as e:
                    last_error = str(e)
                    await asyncio.sleep(1)
            
        raise Exception(f"Ollama failed: {last_error}")
from typing import Optional, Dict
import os
import json
import aiohttp
from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass

class OllamaInterface(LLMInterface):
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        
    async def generate_response(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model_name, "prompt": prompt}
            ) as response:
                if response.status == 200:
                    result = await response.text()
                    return json.loads(result)["response"]
                else:
                    raise Exception(f"Ollama API error: {response.status}")

class OpenAIInterface(LLMInterface):
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.model = model
        
    async def generate_response(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"OpenAI API error: {response.status}")

def create_llm_interface(provider: str = "ollama", **kwargs) -> LLMInterface:
    if provider.lower() == "ollama":
        return OllamaInterface(**kwargs)
    elif provider.lower() == "openai":
        return OpenAIInterface(**kwargs)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
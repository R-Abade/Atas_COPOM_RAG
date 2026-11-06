from abc import ABC, abstractmethod
from typing import List, Dict

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, messages: List[Dict], temperature: float = 0.7):
        pass

class GeminiLLM(BaseLLM):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.5-flash-lite"
    
    def generate(self, messages: List[Dict], temperature: float = 0.3):
        pass

class OllamaLLM(BaseLLM):
    def __init__(self, model: str = "qwen2.5:3b", host: str = "http://localhost:11434"):
        self.host = host
        self.model = model
    
    def generate(self, messages: List[Dict], temperature: float = 0.7):
        pass
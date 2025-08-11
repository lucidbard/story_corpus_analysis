import os
from typing import Optional

class LLMProvider:
    def __init__(self, provider: str, model: str, api_keys: dict):
        self.provider = provider
        self.model = model
        self.api_keys = api_keys
        self.client = None
        self._init_client()

    def _init_client(self):
        if self.provider == 'anthropic':
            try:
                import anthropic
                api_key = self.api_keys.get('anthropic') or os.getenv('ANTHROPIC_API_KEY')
                self.client = anthropic.Anthropic(api_key=api_key) if api_key else None
            except ImportError:
                self.client = None
        elif self.provider == 'openai':
            try:
                import openai
                api_key = self.api_keys.get('openai') or os.getenv('OPENAI_API_KEY')
                self.client = openai.OpenAI(api_key=api_key) if api_key else None
            except ImportError:
                self.client = None
        elif self.provider == 'ollama':
            try:
                import ollama
                self.client = ollama.Client(host='http://localhost:11434')
            except ImportError:
                self.client = None

    def test_connection(self) -> bool:
        # Implement a simple test for each provider
        return self.client is not None

    def get_status(self):
        return {
            'provider': self.provider,
            'model': self.model,
            'client_ready': self.client is not None
        }

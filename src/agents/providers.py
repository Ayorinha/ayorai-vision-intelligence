import os
from dataclasses import dataclass
from typing import Any

import requests

@dataclass(frozen=True)
class LLMConfig:
    base_url: str
    api_key: str
    model: str
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "LLMConfig":
        return cls(
            base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            api_key=os.getenv("LLM_API_KEY", ""),
            model=os.getenv("LLM_MODEL", ""),
            timeout=float(os.getenv("LLM_TIMEOUT_SECONDS", "30")),
        )

class LLMProviderNotConfigured(RuntimeError):
    pass

class OpenAICompatibleProvider:
    """Optional OpenAI-compatible adapter; disabled until credentials are configured."""
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig.from_env()

    @property
    def configured(self) -> bool:
        return bool(self.config.api_key and self.config.model)

    def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> dict[str, Any]:
        if not self.configured:
            raise LLMProviderNotConfigured("Set LLM_API_KEY and LLM_MODEL to enable the provider")
        response = requests.post(
            f"{self.config.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            json={"model": self.config.model, "messages": messages, **kwargs},
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.json()
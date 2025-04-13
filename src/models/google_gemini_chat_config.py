from dataclasses import dataclass
import os

@dataclass(frozen=False)
class GoogleGeminiChatConfig:
    api_key: str = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL")

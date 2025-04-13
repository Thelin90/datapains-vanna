from vanna.google import GoogleGeminiChat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from dataclasses import asdict

from src.models.google_gemini_chat_config import GoogleGeminiChatConfig


class VannaAI(ChromaDB_VectorStore, GoogleGeminiChat):
    def __init__(
        self,
        google_gemini_chat_config: GoogleGeminiChatConfig,
    ) -> None:

        google_gemini_chat_config = asdict(google_gemini_chat_config)
        ChromaDB_VectorStore.__init__(self, config=None)
        GoogleGeminiChat.__init__(
            self,
            config=google_gemini_chat_config
        )

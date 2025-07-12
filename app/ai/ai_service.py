import openai
from app.core.config import get_settings

settings = get_settings()
openai.api_key = settings.openai_api_key

class AIService:
    async def embed_text(self, text: str) -> list[float]:
        """Return a 1536‑dimensional embedding suitable for pgvector."""
        resp = openai.embeddings.create(
            model="text-embedding-3-small", input=text[:8192]
        )
        return resp.data[0].embedding

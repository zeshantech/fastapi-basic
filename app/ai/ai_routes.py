from fastapi import APIRouter
from app.ai.ai_service import AIService

router = APIRouter()


@router.post("/embed")
async def embed(payload: dict):
    return {"embedding": await AIService().embed_text(payload["text"])[:5]}  # trimmed for demo
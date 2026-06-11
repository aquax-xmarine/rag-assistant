from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest
)

from app.services.rag_service import (
    RAGService
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("")
async def chat(
    request: ChatRequest
):

    answer = (
        RAGService().answer(
            request.query,
            request.session_id
        )
    )

    return {
        "answer": answer
    }
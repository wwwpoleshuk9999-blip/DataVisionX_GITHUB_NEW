from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.runtime import runtime


router = APIRouter(tags=["AI"])


class ChatRequest(BaseModel):
    message: str


@router.get("/ai/status")
def ai_status():

    ai = runtime.get_service("ai_service")

    if not ai:
        raise HTTPException(
            status_code=503,
            detail="AI service unavailable"
        )

    return ai.status_info()


@router.post("/ai/chat")
def ai_chat(
    request: ChatRequest
):

    ai = runtime.get_service("ai_service")

    if not ai:
        raise HTTPException(
            status_code=503,
            detail="AI service unavailable"
        )

    return ai.chat(
        request.message
    )

from fastapi import APIRouter
from ai.service import AIService


router = APIRouter()
ai_service = AIService()


@router.get("/ai/status")
def ai_status():
    return ai_service.status_info()


@router.post("/ai/chat")
def ai_chat(message: str):
    return ai_service.chat(message)


@router.get("/ai/history")
def ai_history():
    return ai_service.history()


@router.get("/ai/context")
def ai_context():
    return ai_service.context_info()

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    query: str
    persona: str | None = None


@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    return {"answer": "Chat endpoint ready", "persona": req.persona or "mentor"}


@router.get("/chat/personas")
def list_personas():
    return {"personas": ["mentor", "yoda", "socratic"]}

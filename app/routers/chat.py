from fastapi import APIRouter, Depends
from pydantic import BaseModel

from cgpsc.intelligence.rag_engine import RAGEngine

router = APIRouter(tags=["Chat"])

_rag_engine = None


def get_rag_engine():
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine


class ChatRequest(BaseModel):
    query: str
    persona: str = "mentor"
    k: int = 6
    model: str = "llama3.1:8b"


@router.post("/chat")
def chat_endpoint(req: ChatRequest, rag: RAGEngine = Depends(get_rag_engine)):
    result = rag.chat(
        query=req.query,
        persona=req.persona,
        k=req.k,
        model=req.model,
    )
    return result


@router.get("/chat/history")
def get_chat_history():
    return {"history": []}  # Placeholder for future session management

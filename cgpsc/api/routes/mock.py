from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/mock", tags=["mock"])


class MockGenerateRequest(BaseModel):
    count: int = 100
    subjects: list[str] | None = None


@router.post("/generate")
def generate_mock(req: MockGenerateRequest):
    return {"message": "Mock generation endpoint ready", "count": req.count}

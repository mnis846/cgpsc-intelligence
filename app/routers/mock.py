from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Mock Generator"])


class MockRequest(BaseModel):
    count: int = 100
    subjects: list[str] | None = None
    year_from: int | None = None
    year_to: int | None = None
    difficulties: list[str] | None = None
    shuffle_options: bool = True


@router.post("/mock/generate")
def generate_mock(req: MockRequest):
    # In real use, load questions from your catalog
    return {
        "message": "Mock generation ready. Pass real questions to MockGenerator.",
        "request": req.model_dump(),
    }

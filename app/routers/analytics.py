from fastapi import APIRouter
from pydantic import BaseModel

from cgpsc.intelligence.analytics_engine import AnalyticsEngine

router = APIRouter(tags=["Analytics"])

_analytics = AnalyticsEngine()


class AnalyticsRequest(BaseModel):
    questions: list[dict] | None = None


@router.post("/analytics/compute")
def compute_analytics(req: AnalyticsRequest):
    if req.questions:
        _analytics.set_questions(req.questions)
    return _analytics.compute(force=True)


@router.get("/analytics/snapshot")
def get_snapshot():
    return _analytics.compute()

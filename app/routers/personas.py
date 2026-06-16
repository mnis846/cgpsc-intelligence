from fastapi import APIRouter

from cgpsc.intelligence.personas import list_personas

router = APIRouter(tags=["Personas"])


@router.get("/personas")
def get_personas():
    return {"personas": list_personas()}

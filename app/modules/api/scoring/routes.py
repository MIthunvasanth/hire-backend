from fastapi import APIRouter

from . import service
from .schema import ScoringCreate, ScoringUpdate

router = APIRouter(prefix="/scoring", tags=["Scoring"])


@router.post("/")
async def create_score(payload: ScoringCreate):
    score_id = await service.create_score_service(payload.model_dump())
    return {"id": score_id}


@router.get("/")
async def list_scores():
    return await service.list_scores_service()


@router.get("/{score_id}")
async def get_score(score_id: str):
    return await service.get_score_service(score_id)


@router.put("/{score_id}")
async def update_score(score_id: str, payload: ScoringUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_score_service(score_id, update_data)
    return {"message": "updated"}


@router.delete("/{score_id}")
async def delete_score(score_id: str):
    await service.delete_score_service(score_id)
    return {"message": "deleted"}

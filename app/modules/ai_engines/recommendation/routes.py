from fastapi import APIRouter

from . import service
from .schema import RecommendationCreate, RecommendationUpdate

router = APIRouter(prefix="/recommendations", tags=["Recommendation"])


@router.post("/")
async def create_recommendation(payload: RecommendationCreate):
    recommendation_id = await service.create_recommendation_service(payload.model_dump())
    return {"id": recommendation_id}


@router.get("/")
async def list_recommendations():
    return await service.list_recommendations_service()


@router.get("/{recommendation_id}")
async def get_recommendation(recommendation_id: str):
    return await service.get_recommendation_service(recommendation_id)


@router.put("/{recommendation_id}")
async def update_recommendation(recommendation_id: str, payload: RecommendationUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_recommendation_service(recommendation_id, update_data)
    return {"message": "updated"}


@router.delete("/{recommendation_id}")
async def delete_recommendation(recommendation_id: str):
    await service.delete_recommendation_service(recommendation_id)
    return {"message": "deleted"}

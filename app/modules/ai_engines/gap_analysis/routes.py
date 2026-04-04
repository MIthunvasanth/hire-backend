from fastapi import APIRouter

from . import service
from .schema import GapAnalysisCreate, GapAnalysisUpdate

router = APIRouter(prefix="/gap-analyses", tags=["Gap Analysis"])


@router.post("/")
async def create_gap_analysis(payload: GapAnalysisCreate):
    gap_analysis_id = await service.create_gap_analysis_service(payload.model_dump())
    return {"id": gap_analysis_id}


@router.get("/")
async def list_gap_analyses():
    return await service.list_gap_analyses_service()


@router.get("/{gap_analysis_id}")
async def get_gap_analysis(gap_analysis_id: str):
    return await service.get_gap_analysis_service(gap_analysis_id)


@router.put("/{gap_analysis_id}")
async def update_gap_analysis(gap_analysis_id: str, payload: GapAnalysisUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_gap_analysis_service(gap_analysis_id, update_data)
    return {"message": "updated"}


@router.delete("/{gap_analysis_id}")
async def delete_gap_analysis(gap_analysis_id: str):
    await service.delete_gap_analysis_service(gap_analysis_id)
    return {"message": "deleted"}

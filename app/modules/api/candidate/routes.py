from fastapi import APIRouter

from . import service
from .schema import CandidateCreate, CandidateUpdate

router = APIRouter(prefix="/candidates", tags=["Candidate"])


@router.post("/")
async def create_candidate(payload: CandidateCreate):
    candidate_id = await service.create_candidate_service(payload.model_dump())
    return {"id": candidate_id}


@router.get("/")
async def list_candidates():
    return await service.list_candidates_service()


@router.get("/{candidate_id}")
async def get_candidate(candidate_id: str):
    return await service.get_candidate_service(candidate_id)


@router.put("/{candidate_id}")
async def update_candidate(candidate_id: str, payload: CandidateUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_candidate_service(candidate_id, update_data)
    return {"message": "updated"}


@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: str):
    await service.delete_candidate_service(candidate_id)
    return {"message": "deleted"}

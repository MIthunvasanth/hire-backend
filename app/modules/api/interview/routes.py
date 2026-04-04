from fastapi import APIRouter

from . import service
from .schema import InterviewAgentNextRequest, InterviewCreate, InterviewUpdate

router = APIRouter(prefix="/interviews", tags=["Interview"])


@router.post("/")
async def create_interview(payload: InterviewCreate):
    interview_id = await service.create_interview_service(payload.model_dump())
    return {"id": interview_id}


@router.get("/")
async def list_interviews():
    return await service.list_interviews_service()


@router.get("/{interview_id}")
async def get_interview(interview_id: str):
    return await service.get_interview_service(interview_id)


@router.put("/{interview_id}")
async def update_interview(interview_id: str, payload: InterviewUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    await service.update_interview_service(interview_id, update_data)
    return {"message": "updated"}


@router.delete("/{interview_id}")
async def delete_interview(interview_id: str):
    await service.delete_interview_service(interview_id)
    return {"message": "deleted"}


@router.post("/{interview_id}/agent/next")
async def agent_next(interview_id: str, payload: InterviewAgentNextRequest):
    return await service.agent_next_question_service(interview_id, payload.model_dump())

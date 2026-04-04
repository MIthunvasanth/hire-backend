from fastapi import APIRouter

from . import service
from .schema import TeacherSessionCreate

router = APIRouter(prefix="/ai-teacher", tags=["AI Teacher"])


@router.post("/sessions")
async def create_session(payload: TeacherSessionCreate):
    session_id = await service.create_session_service(payload.model_dump())
    return {"id": session_id}


@router.get("/sessions")
async def list_sessions():
    return await service.list_sessions_service()

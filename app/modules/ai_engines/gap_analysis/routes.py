import logging
import uuid

from fastapi import APIRouter, HTTPException, Query

from . import service
from .schema import GapAnalysisCreate, GapAnalysisHistoryItem, GapAnalysisUpdate, GapAnalyzeRequest, GapAnalyzeResponse

router = APIRouter(prefix="/gap-analyses", tags=["Gap Analysis"])
logger = logging.getLogger(__name__)


@router.post("/")
async def create_gap_analysis(payload: GapAnalysisCreate):
    gap_analysis_id = await service.create_gap_analysis_service(payload.model_dump())
    return {"id": gap_analysis_id}


@router.post("/analyze-live", response_model=GapAnalyzeResponse)
async def analyze_live_gap(payload: GapAnalyzeRequest):
    try:
        return await service.analyze_live_gap_service(payload)
    except ValueError as exc:
        error_id = str(uuid.uuid4())
        message = str(exc)
        logger.warning("gap-analysis value error id=%s message=%s", error_id, message)
        if "LLM request failed" in message:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": message,
                    "code": "GAP_ANALYSIS_LLM_ERROR",
                    "error_id": error_id,
                },
            ) from exc
        raise HTTPException(
            status_code=400,
            detail={
                "message": message,
                "code": "GAP_ANALYSIS_REQUEST_ERROR",
                "error_id": error_id,
            },
        ) from exc
    except Exception as exc:
        error_id = str(uuid.uuid4())
        logger.exception("gap-analysis unexpected error id=%s", error_id)
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Unexpected error during gap analysis",
                "code": "GAP_ANALYSIS_INTERNAL_ERROR",
                "error_id": error_id,
            },
        ) from exc


@router.get("/")
async def list_gap_analyses():
    return await service.list_gap_analyses_service()


@router.get("/history", response_model=list[GapAnalysisHistoryItem])
async def list_gap_analyses_for_user(
    user_id: str | None = Query(default=None),
    user_email: str | None = Query(default=None),
    limit: int = Query(default=30, ge=1, le=100),
):
    if not user_id and not user_email:
        raise HTTPException(status_code=400, detail="Provide user_id or user_email")
    return await service.list_user_gap_analyses_service(user_id=user_id, user_email=user_email, limit=limit)


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

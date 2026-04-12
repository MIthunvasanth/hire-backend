from fastapi import APIRouter, HTTPException, Query

from . import service
from .schema import StudyPlanGenerateRequest, StudyPlanHistoryResponse, StudyPlanResponse, StudyPlanTaskUpdateRequest, StudyReferenceResponse

router = APIRouter(prefix="/ai/study-plan", tags=["AI Study Plan"])


@router.post("/generate", response_model=StudyPlanResponse)
async def generate_study_plan(payload: StudyPlanGenerateRequest):
    try:
        return await service.generate_study_plan_service(
            gap_analysis_id=payload.gap_analysis_id,
            user_id=payload.user_id,
            user_email=payload.user_email,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Study plan generation failed: {exc}") from exc


@router.get("/history", response_model=StudyPlanHistoryResponse)
async def list_study_plans(
    user_id: str | None = Query(default=None),
    user_email: str | None = Query(default=None),
    limit: int = Query(default=30, ge=1, le=100),
):
    if not user_id and not user_email:
        raise HTTPException(status_code=400, detail="Provide user_id or user_email")

    plans = await service.list_study_plans_service(user_id=user_id, user_email=user_email, limit=limit)
    return StudyPlanHistoryResponse(plans=plans)


@router.get("/references", response_model=StudyReferenceResponse)
async def get_study_references(
    query: str = Query(..., min_length=2),
    limit: int = Query(default=6, ge=1, le=12),
):
    try:
        return await service.get_study_references_service(query=query, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Reference search failed: {exc}") from exc


@router.patch("/{plan_id}/task/{task_id}")
async def update_task_completion(plan_id: str, task_id: str, payload: StudyPlanTaskUpdateRequest):
    try:
        await service.update_task_completion_service(plan_id=plan_id, task_id=task_id, completed=payload.completed)
        return {"message": "updated"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Task update failed: {exc}") from exc

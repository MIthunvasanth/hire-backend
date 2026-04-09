from fastapi import APIRouter, HTTPException

from .schema import JobSearchRequest, JobSearchResponse
from .service import search_jobs_service

router = APIRouter(prefix="/ai/job-searcher", tags=["AI Job Searcher"])


@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(payload: JobSearchRequest):
    try:
        return await search_jobs_service(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Job search failed: {exc}") from exc

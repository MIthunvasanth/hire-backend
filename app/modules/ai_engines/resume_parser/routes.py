from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile

from .service import generate_ats_resume, get_latest_ats_for_user, get_latest_parsed_resume, get_parsed_resume_by_id, parse_resume_file
from .schema import ResumeAtsRequest, ResumeAtsResponse, ResumeStoredResponse

router = APIRouter(prefix="/resume-parser", tags=["Resume Parser"])


@router.post("/parse", response_model=ResumeStoredResponse)
async def parse_resume(
    file: UploadFile = File(...),
    user_id: str | None = Form(default=None),
    user_email: str | None = Form(default=None),
):
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise ValueError("Uploaded file is empty.")
        return await parse_resume_file(
            file_name=file.filename or "resume",
            file_bytes=file_bytes,
            content_type=file.content_type,
            user_id=user_id,
            user_email=user_email,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Resume parsing failed: {exc}") from exc


@router.get("/latest", response_model=ResumeStoredResponse)
async def get_latest_resume(
    user_id: str | None = Query(default=None),
    user_email: str | None = Query(default=None),
):
    if not user_id and not user_email:
        raise HTTPException(status_code=400, detail="Provide user_id or user_email")

    item = await get_latest_parsed_resume(user_id=user_id, user_email=user_email)
    if not item:
        raise HTTPException(status_code=404, detail="No parsed resume found")
    return item


@router.get("/{resume_id}", response_model=ResumeStoredResponse)
async def get_resume_by_id(resume_id: str):
    item = await get_parsed_resume_by_id(resume_id)
    if not item:
        raise HTTPException(status_code=404, detail="Parsed resume not found")
    return item


@router.post("/ats", response_model=ResumeAtsResponse)
async def create_ats_resume(payload: ResumeAtsRequest):
    try:
        if not payload.resume_id and not payload.user_id and not payload.user_email:
            raise ValueError("Provide resume_id or user_id/user_email to run ATS optimization")
        return await generate_ats_resume(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"ATS optimization failed: {exc}") from exc


@router.get("/ats/latest", response_model=ResumeAtsResponse)
async def get_latest_ats(
    user_id: str | None = Query(default=None),
    user_email: str | None = Query(default=None),
):
    if not user_id and not user_email:
        raise HTTPException(status_code=400, detail="Provide user_id or user_email")

    item = await get_latest_ats_for_user(user_id=user_id, user_email=user_email)
    if not item:
        raise HTTPException(status_code=404, detail="No ATS optimization found")
    return item

import asyncio
import logging
import sys
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.core.config import settings

from app.modules.auth.routes import router as auth_router
from app.modules.api.admin.routes import router as admin_router
from app.modules.ai_engines.ai_teacher.routes import router as ai_teacher_router
from app.modules.ai_engines.job_searcher.routes import router as job_searcher_router
from app.modules.ai_engines.resume_parser.routes import router as resume_parser_router
from app.modules.ai_engines.scraper.routes import router as scraper_router
from app.modules.ai_engines.study_plan.routes import router as study_plan_router
from app.modules.api.application.routes import router as application_router
from app.modules.api.candidate.routes import router as candidate_router
from app.modules.api.dashboard.routes import router as dashboard_router
from app.modules.ai_engines.gap_analysis.routes import router as gap_analysis_router
from app.modules.api.interview.routes import router as interview_router
from app.modules.api.job.routes import router as job_router
from app.modules.ai_engines.recommendation.routes import router as recommendation_router
from app.modules.api.recruiter.routes import router as recruiter_router
from app.modules.api.resume.routes import router as resume_router
from app.modules.api.scoring.routes import router as scoring_router
from app.modules.api.user.routes import router as user_router
from app.modules.api.coding.routes import router as coding_router

if sys.platform.startswith("win"):
	# Playwright launches a browser subprocess and requires Proactor loop on Windows.
	asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI(title="urselected Backend")
logger = logging.getLogger(__name__)


def _normalize_error_detail(status_code: int, detail: object, path: str) -> dict:
	error_id = str(uuid.uuid4())
	code = f"HTTP_{status_code}"
	message = "Request failed"
	debug = None

	if isinstance(detail, dict):
		message = str(detail.get("message") or detail.get("detail") or message)
		code = str(detail.get("code") or code)
		error_id = str(detail.get("error_id") or error_id)
		debug = detail.get("debug")
	else:
		message = str(detail or message)

	payload = {
		"message": message,
		"code": code,
		"error_id": error_id,
		"path": path,
	}
	if debug:
		payload["debug"] = str(debug)
	return payload

allowed_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
app.add_middleware(
	CORSMiddleware,
	allow_origins=allowed_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
	detail = _normalize_error_detail(exc.status_code, exc.detail, request.url.path)
	return JSONResponse(status_code=exc.status_code, content={"detail": detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	detail = _normalize_error_detail(
		422,
		{
			"message": "Request validation failed",
			"code": "VALIDATION_ERROR",
			"debug": exc.errors(),
		},
		request.url.path,
	)
	return JSONResponse(status_code=422, content={"detail": detail})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
	error_id = str(uuid.uuid4())
	logger.exception("Unhandled server error id=%s path=%s", error_id, request.url.path)
	return JSONResponse(
		status_code=500,
		content={
			"detail": {
				"message": "Internal server error",
				"code": "INTERNAL_SERVER_ERROR",
				"error_id": error_id,
				"path": request.url.path,
				"debug": str(exc),
			}
		},
	)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(candidate_router)
app.include_router(recruiter_router)
app.include_router(admin_router)
app.include_router(resume_router)
app.include_router(job_router)
app.include_router(application_router)
app.include_router(gap_analysis_router)
app.include_router(recommendation_router)
app.include_router(interview_router)
app.include_router(scoring_router)
app.include_router(dashboard_router)
app.include_router(ai_teacher_router)
app.include_router(job_searcher_router)
app.include_router(resume_parser_router)
app.include_router(scraper_router)
app.include_router(study_plan_router)
app.include_router(coding_router)


if __name__ == "__main__":
	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

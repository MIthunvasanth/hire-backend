from fastapi import FastAPI

from app.modules.auth.routes import router as auth_router
from app.modules.api.admin.routes import router as admin_router
from app.modules.ai_engines.ai_teacher.routes import router as ai_teacher_router
from app.modules.ai_engines.scraper.routes import router as scraper_router
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

app = FastAPI(title="Hire Backend")

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
app.include_router(scraper_router)

from pydantic import BaseModel, Field


class JobSearchRequest(BaseModel):
    query: str = Field(min_length=2)
    page: int = Field(default=1, ge=1, le=50)
    num_pages: int = Field(default=1, ge=1, le=50)
    country: str = Field(default="us", min_length=2, max_length=2)
    language: str | None = None
    location: str | None = None
    date_posted: str = Field(default="all")
    work_from_home: bool = False
    employment_types: str | None = None
    job_requirements: str | None = None
    radius: float | None = Field(default=None, ge=0)
    exclude_job_publishers: str | None = None
    fields: str | None = None


class JobCard(BaseModel):
    job_id: str
    title: str
    company: str
    location: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    is_remote: bool = False
    employment_type: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None
    posted_at: str | None = None
    posted_human_readable: str | None = None
    apply_link: str | None = None
    publisher: str | None = None


class JobDetails(JobCard):
    description: str | None = None
    apply_options: list[dict] = Field(default_factory=list)
    highlights: dict = Field(default_factory=dict)


class JobSearchResponse(BaseModel):
    status: str
    query: str
    page: int
    total_results: int
    jobs: list[JobDetails]

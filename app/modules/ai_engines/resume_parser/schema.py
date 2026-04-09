from pydantic import BaseModel, Field


class ResumeSkill(BaseModel):
    name: str
    level: str | None = None


class ResumeExperience(BaseModel):
    title: str
    company: str
    duration: str
    location: str | None = None
    description: str | None = None


class ResumeEducation(BaseModel):
    institution: str
    degree: str
    duration: str | None = None
    details: str | None = None


class ResumeProject(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)


class ResumeCertification(BaseModel):
    name: str
    issuer: str | None = None
    year: str | None = None


class ResumeBasics(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    linkedin: str | None = None
    portfolio: str | None = None


class ResumeParseSections(BaseModel):
    basics: ResumeBasics = Field(default_factory=ResumeBasics)
    summary: str | None = None
    skills: list[ResumeSkill] = Field(default_factory=list)
    experience: list[ResumeExperience] = Field(default_factory=list)
    education: list[ResumeEducation] = Field(default_factory=list)
    projects: list[ResumeProject] = Field(default_factory=list)
    certifications: list[ResumeCertification] = Field(default_factory=list)


class ResumeParseResponse(BaseModel):
    file_name: str
    file_type: str
    raw_text_excerpt: str
    sections: ResumeParseSections


class ResumeStoredResponse(ResumeParseResponse):
    id: str
    user_id: str | None = None
    user_email: str | None = None
    created_at: str


class AtsContext(BaseModel):
    job_title: str | None = None
    company_name: str | None = None
    extracted_jd_keywords: list[str] = Field(default_factory=list)
    experience_level: str | None = None
    industry: str | None = None


class AtsScoreBreakdown(BaseModel):
    score: int
    keyword_match: int
    format_score: int
    impact_score: int
    missing_keywords: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class AtsContact(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""


class AtsExperienceItem(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    location: str = ""
    bullets: list[str] = Field(default_factory=list)


class AtsEducationItem(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""
    gpa: str = ""
    relevant_coursework: list[str] = Field(default_factory=list)


class AtsSkills(BaseModel):
    technical: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    soft: list[str] = Field(default_factory=list)
    suggested: list[str] = Field(default_factory=list)


class AtsProjectItem(BaseModel):
    name: str = ""
    tech_stack: list[str] = Field(default_factory=list)
    description: str = ""
    link: str = ""


class ResumeAtsResult(BaseModel):
    summary: str = ""
    contact: AtsContact = Field(default_factory=AtsContact)
    experience: list[AtsExperienceItem] = Field(default_factory=list)
    education: list[AtsEducationItem] = Field(default_factory=list)
    skills: AtsSkills = Field(default_factory=AtsSkills)
    projects: list[AtsProjectItem] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    ats_score: AtsScoreBreakdown


class ResumeAtsRequest(BaseModel):
    resume_id: str | None = None
    user_id: str | None = None
    user_email: str | None = None
    target_context: AtsContext = Field(default_factory=AtsContext)


class ResumeAtsResponse(BaseModel):
    id: str
    resume_id: str
    user_id: str | None = None
    user_email: str | None = None
    created_at: str
    target_context: AtsContext = Field(default_factory=AtsContext)
    result: ResumeAtsResult

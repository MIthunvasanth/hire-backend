from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    users: int
    candidates: int
    jobs: int
    applications: int

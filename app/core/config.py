from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mongo_url: str = Field(default="mongodb://localhost:27017", alias="MONGO_URI")
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")
    mongo_db_name: str = Field(default="career_ai", alias="MONGO_DB")
    cors_origins: str = Field(
        default="http://localhost:8080,http://127.0.0.1:8080,https://urselected.netlify.app",
        alias="CORS_ORIGINS",
    )
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_resume_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_RESUME_MODEL")
    openai_gap_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_GAP_MODEL")
    resume_parser_max_chars: int = Field(default=18000, alias="RESUME_PARSER_MAX_CHARS")
    rapidapi_key: str | None = Field(default=None, alias="RAPIDAPI_KEY")
    rapidapi_host: str = Field(default="jsearch.p.rapidapi.com", alias="RAPIDAPI_HOST")
    rapidapi_base_url: str = Field(default="https://jsearch.p.rapidapi.com", alias="RAPIDAPI_BASE_URL")
    searxng_base_url: str = Field(default="http://127.0.0.1:8081", alias="SEARXNG_BASE_URL")
    searxng_timeout_seconds: float = Field(default=20.0, alias="SEARXNG_TIMEOUT_SECONDS")


settings = Settings()

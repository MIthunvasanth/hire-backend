from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mongo_url: str = Field(default="mongodb://localhost:27017", alias="MONGO_URI")
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")
    mongo_db_name: str = Field(default="career_ai", alias="MONGO_DB")


settings = Settings()

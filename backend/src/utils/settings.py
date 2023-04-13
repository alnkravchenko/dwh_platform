from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field(env="APP_NAME", default="FastAPI")
    version: str = Field(env="APP_VERSION", default="0.0")
    database_url: str = Field(env="DB_URL", default="sqlite:///./sql_app.db")
    origins: List[str] = Field(
        env="ORIGINS", default=["http://localhost:8000", "http://localhost:5000"]
    )


settings = Settings()

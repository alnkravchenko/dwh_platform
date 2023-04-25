from typing import List

from pydantic import BaseSettings, Field, NonNegativeInt


class Settings(BaseSettings):
    APP_NAME: str = Field(env="APP_NAME", default="FastAPI")
    VERSION: str = Field(env="APP_VERSION", default="0.0")
    DATABASE_URL: str = Field(
        env="DB_URL", default="sqlite:///./sql_app.db", repr=False
    )
    ORIGINS: List[str] = Field(
        env="ORIGINS", default=["http://localhost:8000", "http://localhost:5000"]
    )
    ACCESS_TOKEN_EXPIRE_MIN: NonNegativeInt = Field(
        env="ACCESS_TOKEN_EXPIRE", default=90
    )
    JWT_SECRET_KEY: str = Field(env="JWT_SECRET_KEY", default="", repr=False)


settings = Settings()

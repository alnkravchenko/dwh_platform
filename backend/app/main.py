from typing import List

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings, Field
from routers import auth


class Settings(BaseSettings):
    app_name: str = Field(env="APP_NAME", default="FastAPI")
    version: str = Field(env="APP_VERSION", default="0.0")
    origins: List[str] = Field(env="ORIGINS", default=["http://localhost:8000", "http://localhost:5000"])

# create and configure the app
app = FastAPI()
settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routings
app.include_router(auth.router)


log = structlog.get_logger()
log.info(f"App started with configs:\n{settings}")

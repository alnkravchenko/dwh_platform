from typing import List

import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.base import Base
from pydantic import BaseSettings, Field
from repos.database import engine
from routers import auth


class Settings(BaseSettings):
    app_name: str = Field(env="APP_NAME", default="FastAPI")
    version: str = Field(env="APP_VERSION", default="0.0")
    origins: List[str] = Field(
        env="ORIGINS", default=["http://localhost:8000", "http://localhost:5000"]
    )


# Database connection
Base.metadata.create_all(bind=engine)

# Create and configure the app
app = FastAPI()
settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    error_details = exc.errors()
    msg = error_details[0]["msg"].capitalize()
    return JSONResponse(content={"details": msg}, status_code=400)


# Routings
app.include_router(auth.router)


# Logging
log = structlog.get_logger(module=__name__)
log.info(f"App started with configs:\n{settings}")

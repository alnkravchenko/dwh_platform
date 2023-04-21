import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.base import Base
from repos.database import engine
from routers import auth
from utils import settings as config

# Database connection
Base.metadata.create_all(bind=engine)

# Create and configure the app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.settings.ORIGINS,
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
log.info(f"App started with configs:\n{config.settings}")

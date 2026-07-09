"""FastAPI application entrypoint.

Run locally with:
    uvicorn app.main:app --reload

Routers are intentionally NOT wired up yet — this phase only proves the
skeleton boots, connects its middleware/logging correctly, and exposes a
health check. Each later phase adds its own router here with one new line.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine
from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown hook. Cleans up the DB connection pool on exit."""
    logger.info("Starting %s [env=%s, debug=%s]", settings.PROJECT_NAME, settings.ENV, settings.DEBUG)
    yield
    logger.info("Shutting down %s", settings.PROJECT_NAME)
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="AI-powered receptionist backend for appointment-based clinics.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all so unexpected errors never leak a raw traceback to a client,
    while still being fully logged server-side for debugging.
    """
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


@app.get("/", tags=["Root"])
async def root() -> dict:
    return {"message": f"{settings.PROJECT_NAME} API", "status": "ok"}


@app.get("/health", tags=["Root"])
async def health_check() -> dict:
    """Liveness/readiness probe for Docker/Railway/Azure health checks."""
    return {"status": "healthy", "env": settings.ENV}


# --- Routers ---------------------------------------------------------------
# Each feature phase registers its router here, e.g.:
#
#   from app.routes import chat, appointments, patients, knowledge
#   app.include_router(chat.router, prefix=settings.API_V1_PREFIX, tags=["Chat"])
#   app.include_router(appointments.router, prefix=settings.API_V1_PREFIX, tags=["Appointments"])

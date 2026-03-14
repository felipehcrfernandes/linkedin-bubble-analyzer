from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.database import create_tables
from backend.routes.health import router as health_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    create_tables()
    yield


def create_app() -> FastAPI:
    application = FastAPI(title="LinkedIn Bubble Analyzer", lifespan=lifespan)
    application.include_router(health_router)
    return application


app = create_app()

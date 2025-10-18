import time
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core.config import settings
from app.core.errors import (
    HiggsFieldAPIError,
    generic_exception_handler,
    higgsfield_api_error_handler,
    http_exception_handler,
)
from app.core.logging import get_logger, setup_logging
from app.routers import health, i2v, jobs, t2i, t2v

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(
        "app_startup",
        app_name=settings.app_name,
        env=settings.app_env,
        debug=settings.app_debug,
    )
    yield
    logger.info("app_shutdown")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-grade FastAPI wrapper for Higgsfield multimodal generation APIs",
    docs_url="/docs" if settings.app_debug else None,
    redoc_url="/redoc" if settings.app_debug else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next: Any) -> Any:
    start_time = time.time()

    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
    )

    try:
        response = await call_next(request)

        duration = time.time() - start_time
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=int(duration * 1000),
        )

        return response

    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "request_failed",
            method=request.method,
            path=request.url.path,
            duration_ms=int(duration * 1000),
            error=str(e),
        )
        raise

app.add_exception_handler(HiggsFieldAPIError, higgsfield_api_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(health.router)
app.include_router(t2v.router)
app.include_router(i2v.router)
app.include_router(t2i.router)
app.include_router(jobs.router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.app_debug,
        log_level=settings.log_level.lower(),
    )


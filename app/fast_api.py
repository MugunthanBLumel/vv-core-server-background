from logging import Logger
from typing import Any

import sqltap
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v2.api import v2_api_router
from app.conf.config import settings


def init_fast_api_app(logger: Logger) -> FastAPI:
    # API Server Init
    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        debug=True,
    )
    app.extra["logger"] = logger

    # API Server Middleware config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(v2_api_router, prefix=settings.API_PREFIX)

    @app.middleware("http")
    async def add_sql_tap(request: Request, call_next):
        profiler = sqltap.start()
        response = await call_next(request)
        statistics = profiler.collect()
        sqltap.report(statistics, "report.html", report_format="html")
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                {
                    "detail": {
                        "message": "invalid request",
                        "error_description": str(exc),
                    }
                }
            ),
        )

    # Default API Server Route with Health Check
    @app.get("/")
    def health_check(request: Request) -> Any:
        request.app.extra.get("logger").info("Health Check API Called")
        return {"msg": "Hello Universe...!"}

    return app

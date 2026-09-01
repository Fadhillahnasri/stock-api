from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.exceptions.provider_exceptions import (
    ProviderError,
    ProviderTimeoutError,
    ProviderConnectionError
)

from app.utils.logger import logger


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):

    logger.warning(
        f"{request.method} {request.url.path} -> {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status": exc.status_code,
            "message": exc.detail,
            "path": request.url.path,
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
    ):

    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "status": 500,
            "message": "Internal Server Error",
            "path": request.url.path,
        },
    )

async def provider_exception_handler(
    request: Request,
    exc: ProviderError
):

    logger.exception(
        f"Provider Error - {request.url.path}: {exc}"
    )

    return JSONResponse(
        status_code=502,
        content={
            "success": False,
            "status": 502,
            "message": str(exc),
            "path": request.url.path
        }
    )
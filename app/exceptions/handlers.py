from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

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
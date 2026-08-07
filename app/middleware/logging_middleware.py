import time

from fastapi import Request

from app.utils.logger import logger


async def logging_middleware(request: Request, call_next):

    start_time = time.perf_counter()

    logger.info(
        f"Incoming Request | {request.method} {request.url.path}"
    )

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    logger.info(
        f"Completed | Status={response.status_code} | Time={process_time:.3f}s"
    )

    return response
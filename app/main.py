from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.api.websocket import router as websocket_router

from fastapi import HTTPException

from app.exceptions.provider_exceptions import ProviderError

from app.exceptions.handlers import (
    http_exception_handler,
    generic_exception_handler,
    provider_exception_handler,
)

from app.middleware.logging_middleware import logging_middleware


app = FastAPI(
    title="Indonesia Stock API",
    version="1.0.0"
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    ProviderError,
    provider_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

app.middleware("http")(logging_middleware)

templates = Jinja2Templates(directory="templates")


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


app.include_router(router)
app.include_router(websocket_router)
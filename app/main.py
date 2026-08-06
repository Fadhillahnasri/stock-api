from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.api.websocket import router as websocket_router

app = FastAPI(
    title="Indonesia Stock API",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


app.include_router(router)
app.include_router(websocket_router)
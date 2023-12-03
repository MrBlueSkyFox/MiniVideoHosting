from fastapi import FastAPI, Request
# from api import video_router
from starlette.templating import Jinja2Templates

from app.api.api import api_router
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

app.include_router(api_router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

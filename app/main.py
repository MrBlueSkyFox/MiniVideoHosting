from fastapi import FastAPI
# from api import video_router
from app.api.api import video_router

app = FastAPI()

app.include_router(video_router)


@app.get("/")
async def root():
    return {"message": "rootdev"}

from fastapi import APIRouter

from app.api.endpoints import video

api_router = APIRouter()
api_router.include_router(video.video_router, prefix="/video", tags=["video"])

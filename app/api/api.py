from fastapi import APIRouter

from app.api.endpoints import video, user, auth

api_router = APIRouter()
api_router.include_router(video.video_router, prefix="/video", tags=["video"])
api_router.include_router(user.user_router, prefix="/user", tags=["user"])
api_router.include_router(auth.auth_router, prefix="/auth", tags=["auth"])

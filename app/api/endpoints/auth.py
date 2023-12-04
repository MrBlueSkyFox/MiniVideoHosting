from fastapi import APIRouter

from core.fast_api_users import auth_backend, fastapi_users_point

auth_router = APIRouter()
auth_router.include_router(
    fastapi_users_point.get_auth_router(auth_backend), prefix="/jwt", tags=["auth"]
)

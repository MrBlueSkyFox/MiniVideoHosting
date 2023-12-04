from fastapi import Depends, APIRouter

from api.deps import current_active_user, fastapi_users_point
from app.models.user import User
from app.shemas.user import UserRead, UserCreate, UserUpdate

user_router = APIRouter()

user_router.include_router(
    fastapi_users_point.get_register_router(UserRead, UserCreate),
    tags=["user"],
)
user_router.include_router(
    fastapi_users_point.get_reset_password_router(),
    prefix="/auth",
    tags=["user"],
)

user_router.include_router(
    fastapi_users_point.get_users_router(UserRead, UserUpdate),
    prefix="/user",
    tags=["user"],
)


@user_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

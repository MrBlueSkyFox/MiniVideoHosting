import uuid

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.api.deps import get_user_db
from app.models.user import User
from app.core.config import settings
from app.crud.user_manager import UserManager

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users_point = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

from uuid import UUID
from typing import Optional

from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr


class UserRead(schemas.BaseUser[UUID]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]


class UserInDb(schemas.BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: EmailStr
    password: str
    username: str

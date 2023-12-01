from typing import Optional
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class VideoIn(BaseModel):
    title: str
    description: str
    filename: str
    # file: Optional[str]


class VideoUpdate(BaseModel):
    name: str
    description: str


class VideoInDBBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    filename: str


class Video(VideoInDBBase):
    pass

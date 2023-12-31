from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VideoIn(BaseModel):
    title: str
    description: str
    filename: str
    owner_id: UUID


class VideoUpdate(BaseModel):
    title: str = None
    description: str = None


class VideoInDBBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    title: str
    description: str
    filename: str


class Video(VideoInDBBase):
    pass

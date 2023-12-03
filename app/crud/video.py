from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.video import Video
from app.shemas.video import VideoIn, VideoUpdate


class CRUDVideo(CRUDBase[Video, VideoIn, VideoUpdate]):
    async def create(
            self,
            db_session: AsyncSession,
            video_in: VideoIn
    ) -> Video:
        db_obj = Video(**video_in.model_dump())
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def get(
            self,
            db_session: AsyncSession,
            id: UUID
    ) -> Video:
        # video_obj = await db_session.query(Video).filter(Video.id == id).first()
        stmt = select(Video).where(Video.id == id)
        video_obj = await db_session.execute(stmt)
        video_obj = video_obj.scalars().first()
        return video_obj

    async def get_all(
            self,
            db_session: AsyncSession
    ) -> list[Video]:
        stmt = select(Video)
        video_objects = await db_session.execute(stmt)
        video_objects = video_objects.scalars()
        return video_objects

    async def update(
            self,
            db_session: AsyncSession,
            video_obj: Video, video_update: VideoUpdate
    ) -> Video:
        obj_data = jsonable_encoder(video_obj)
        update_data = video_update.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(video_obj, field, update_data[field])
        db_session.add(video_obj)
        await db_session.commit()
        await db_session.refresh(video_obj)
        return video_obj

    async def remove(
            self,
            db_session: AsyncSession,
            video_obj: Video
    ) -> Video:
        await db_session.delete(video_obj)
        await db_session.commit()
        return video_obj


video = CRUDVideo(Video)

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.video import Video
from app.shemas.video import VideoIn, VideoUpdate


class CRUDVideo(CRUDBase[Video, VideoIn, VideoUpdate]):
    async def create_video(self,
                           db_session: AsyncSession,
                           video_in: VideoIn) -> Video:
        db_obj = Video(**video_in.model_dump())
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def get_video(self,
                        db_session: AsyncSession,
                        id: UUID) -> Video:
        # video_obj = await db_session.query(Video).filter(Video.id == id).first()
        stmt = select(Video).where(Video.id == id)
        video_obj = await db_session.execute(stmt)
        video_obj = video_obj.scalars().first()
        return video_obj


video = CRUDVideo(Video)

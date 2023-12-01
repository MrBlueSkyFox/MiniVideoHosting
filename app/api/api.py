import os
import shutil
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, Form, Header

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.engine import get_session
from app.shemas.video import VideoIn, VideoUpdate, Video

video_router = APIRouter()
SAVE_DIR = r"C:\Users\Tigran\PycharmProjects\MiniVideoHosting\data"


@video_router.post("/", response_model=Video)
async def create_video(
        back_tasks: BackgroundTasks,
        # video_in: VideoIn,
        file: UploadFile = File(...),
        name: str = Form(...),
        description: str = Form(...),
        db: AsyncSession = Depends(get_session),
):
    video_in = VideoIn(filename=file.filename, title=name, description=description)
    video = await crud.video.create_video(db, video_in)
    file_name = str(video.id) + video_in.filename
    back_tasks.add_task(write_video, file, file_name)
    return video


@video_router.get("/video")
async def get_all_video():
    pass


async def get_video_by_user():
    pass

CHUNK_SIZE = 1024*1024
@video_router.get("/{id}")
async def get_video(id: UUID, range: str = Header(None)):
    video = await  crud.video.get_video(id)
    video_path = set
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")


@video_router.put("/{id}")
async def update_video():
    pass


@video_router.delete("/{id}")
async def delete_video():
    pass


def write_video(file, file_name: str):
    file_name = os.path.join(SAVE_DIR, file_name)
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

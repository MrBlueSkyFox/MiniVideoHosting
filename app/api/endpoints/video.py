import os
import shutil
from pathlib import Path
from typing import IO, Generator
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, Form, Header, Response, Request

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import StreamingResponse, Response
from starlette.templating import Jinja2Templates


from app import crud
from app.db.engine import get_session
from app.shemas.video import VideoIn, VideoUpdate, Video
from db.engine import get_session
from shemas.video import Video, VideoIn

templates = Jinja2Templates(directory="templates")

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


CHUNK_SIZE = 1024 * 1024


@video_router.get("/stream/{id}")
async def get_streaming_video(id: UUID, request: Request, db: AsyncSession = Depends(get_session)) -> StreamingResponse:
    video = await crud.video.get_video(db, id)

    video_path_file = str(video.id) + video.filename
    video_path_file = os.path.join(SAVE_DIR, video_path_file)
    file, status_code, content_length, headers = await open_file(request, video_path_file)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response


@video_router.get("/stream2/{id}")
async def get_video(id: UUID, range: str = Header(None), db: AsyncSession = Depends(get_session)):
    video = await crud.video.get_video(db, id)
    video_path = str(video.id) + video.filename
    video_path = os.path.join(SAVE_DIR, video_path)
    video_path = Path(video_path)
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


async def open_file(request: Request, file_path: str) -> tuple:
    path = Path(file_path)
    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


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

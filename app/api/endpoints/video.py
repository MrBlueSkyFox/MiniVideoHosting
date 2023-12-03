from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, Form, Header

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import StreamingResponse, Response
from starlette.templating import Jinja2Templates

from app import crud
from db.engine import get_session
from services.video import open_file, write_video, get_absolute_file_path
from shemas.video import Video, VideoIn

CHUNK_SIZE = 1024 * 1024
templates = Jinja2Templates(directory="templates")

video_router = APIRouter()


@video_router.post("/", response_model=Video)
async def create_video(
        back_tasks: BackgroundTasks,
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


@video_router.get("/stream/{id}")
async def get_streaming_video(id: UUID, request: Request, db: AsyncSession = Depends(get_session)) -> StreamingResponse:
    video = await crud.video.get_video(db, id)

    video_file_name = str(video.id) + video.filename
    video_file_name = get_absolute_file_path(video_file_name)
    file, status_code, content_length, headers = await open_file(request, video_file_name)
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
    video_file_name = str(video.id) + video.filename
    video_abs_file_name = get_absolute_file_path(video_file_name)
    video_abs_file_name = Path(video_abs_file_name)
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_abs_file_name, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_abs_file_name.stat().st_size)
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

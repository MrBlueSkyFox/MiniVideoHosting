import os
import shutil
from pathlib import Path
from typing import IO, Generator

from starlette.requests import Request

SAVE_DIR = r"C:\Users\Tigran\PycharmProjects\MiniVideoHosting\data"


async def get_video_by_user():
    pass


def get_absolute_file_path(relative_path: str) -> str:
    return os.path.join(SAVE_DIR, relative_path)


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


def write_video(file, file_name: str):
    file_name = os.path.join(SAVE_DIR, file_name)
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

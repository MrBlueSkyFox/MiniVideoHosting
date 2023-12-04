from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings

connect_args = {"check_same_thread": False}
engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    future=True,
    poolclass=NullPool,
)


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        yield session

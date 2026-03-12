from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from korochki.core.config import get_settings
from korochki.db.base import Base

settings = get_settings()

engine = create_async_engine(settings.ASYNC_DATABSE_URL)

async_session_maker =async_sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with async_session_maker() as session:
        yield session
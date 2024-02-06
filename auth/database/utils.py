from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from auth.models.base import Base
from config import config


engine = create_async_engine(config.DB_URL, echo=True)
AsyncLocalSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def session_factory() -> AsyncSession:
    async with AsyncLocalSession() as session:
        yield session


def async_session(func):
    async def wrapper(*args, **kwargs):
        async with session_factory() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper


@async_session
async def db_setup(session) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

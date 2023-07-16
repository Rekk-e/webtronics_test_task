from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

ASYNC_URI = settings.SQLALCHEMY_DATABASE_URI.replace('postgresql', 'postgresql+asyncpg')

engine = create_async_engine(
    ASYNC_URI, pool_pre_ping=True, max_overflow=-1
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

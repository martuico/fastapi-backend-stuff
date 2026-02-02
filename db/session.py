import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://mar-tuico:password@localhost:5432/queue_db")
DB_ECHO = os.getenv("DB_DEBUG", "False").lower() in ("true", "1", "yes")

engine = create_async_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ------------------------
# Dependency for FastAPI
# ------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator dependency for FastAPI.
    Use: `db: AsyncSession = Depends(get_db)` in your endpoints.
    """
    async with AsyncSessionLocal() as session:
        yield session

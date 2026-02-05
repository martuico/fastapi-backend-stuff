from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import Settings

settings = Settings()

DATABASE_URL = settings.DATABASE_URL
DB_ECHO = settings.DB_DEBUG

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

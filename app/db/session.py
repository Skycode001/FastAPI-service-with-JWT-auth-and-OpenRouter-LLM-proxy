from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True if settings.ENV == "local" else False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
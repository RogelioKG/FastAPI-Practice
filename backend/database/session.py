from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from models.base import Base

engine = create_async_engine(
    settings.get_settings().database_uri,
    # connection pool 的 connection 數量 (預設 5)
    pool_size=50,
    # 容許多出的 connection 數量 (預設 10)
    max_overflow=50,
    # 當 connection pool 沒有 connection 時，願意等多久來拿 connection (預設 30)
    pool_timeout=40,
    # 當一條 connection 存在超過幾秒時，主動關掉並分配一條新連線 (預設 -1)
    pool_recycle=1800,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_db() -> None:
    await engine.dispose()

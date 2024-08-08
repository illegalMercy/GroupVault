from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import config
from .models import Base
from .crud.create import create_admin, create_price


__all__ = ['create_db', 'async_session']


def create_engine(db_fp: Path):
    if not db_fp.parent.exists():
        db_fp.parent.mkdir(parents=True)
        
    database_url = 'sqlite+aiosqlite:///' + str(db_fp.absolute())
    engine = create_async_engine(database_url, echo=False)
    return engine


def create_async_session():
    return async_sessionmaker(engine)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
async def init_db():
    await create_admin(async_session, config.admin_id)

    prices = [(i+1, (i+1)*100) for i in range(12)]
    for month, price in prices:
        await create_price(async_session, month, price)


engine = create_engine(config.sqlite_database_path)
async_session = create_async_session()

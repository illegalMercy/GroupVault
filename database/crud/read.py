from database.models import *
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def get_admin(async_session: async_sessionmaker[AsyncSession], 
                    user_id: int) -> Admin | None:
    async with async_session() as session:
        result = await session.execute(select(Admin).where(Admin.id == user_id))
        
    admin = result.scalar_one_or_none()
    return admin is not None


async def get_sessions(async_session: async_sessionmaker[AsyncSession]) -> list[Session]:
    async with async_session() as session:
        result = await session.execute(select(Session))
    sessions = result.scalars().unique().all()
    return sessions


async def get_session(async_session: async_sessionmaker[AsyncSession], 
                              session_id: int | None = None, name: str | None = None) -> Session:
    
    if session_id is None and name is None:
        raise ValueError("You must specify either session_id or name")
    
    filter = Session.id if session_id else Session.name

    async with async_session() as session:
        result = await session.execute(
            select(Session).
            where(filter == (session_id if session_id else name))
        )
    session = result.scalar_one_or_none()
    return session


async def get_free_groups(async_session: async_sessionmaker[AsyncSession]) -> list[Group]:
    async with async_session() as session:
        result = await session.execute(
            select(Group).
            where(Group.buyer_id == None)
        )
    groups = result.scalars().unique().all()
    return groups


async def get_prices(async_session: async_sessionmaker[AsyncSession]) -> list[Price]:
    async with async_session() as session:
        result = await session.execute(select(Price))
    prices = result.scalars().unique().all()
    return prices

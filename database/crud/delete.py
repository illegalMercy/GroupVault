from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from ..models import Session, Group, Price


async def delete_session(async_session: async_sessionmaker[AsyncSession], 
                         session_name: str):
    async with async_session() as session:
        await session.execute(
            delete(Session)
            .where(Session.name == session_name)
        )
        await session.commit()

async def delete_groups(async_session: async_sessionmaker[AsyncSession], group_ids: list):
    async with async_session() as session:
        for i in group_ids:
            await session.execute(
                delete(Group)
                .where(Group.id == i)
            )
        await session.commit()


async def delete_price(async_session: async_sessionmaker[AsyncSession], group_age: int):
    async with async_session() as session:
        await session.execute(
            delete(Price)
            .where(Price.age == group_age)
        )
        await session.commit()
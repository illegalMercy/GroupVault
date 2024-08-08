from database.models import *
from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def update_group_buyer(async_session: async_sessionmaker[AsyncSession], 
                             buyer_id: int, group_id: int):
    async with async_session() as session:
        await session.execute(
            update(Group).
            where(Group.id == group_id).
            values(buyer_id = buyer_id)
        )
        await session.commit()


async def update_price(async_session: async_sessionmaker[AsyncSession], 
                       age: int, price: float):
    async with async_session() as session:
        await session.execute(
            update(Price).
            where(Price.age == age).
            values(price = price)
        )
        await session.commit()



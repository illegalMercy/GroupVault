from database.models import *
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def create_user(async_session: async_sessionmaker[AsyncSession], user_id: int) -> User:
    async with async_session() as session:
        existing_user = await session.get(User, user_id)
        if existing_user is not None:
            return existing_user
        
        new_user = User(id=user_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return new_user


async def create_admin(async_session: async_sessionmaker[AsyncSession], user_id: int) -> Admin:
    async with async_session() as session:
        existing_user = await session.get(Admin, user_id)
        if existing_user is not None:
            return existing_user
        
        new_admin = Admin(id=user_id)
        session.add(new_admin)
        await session.commit()
        await session.refresh(new_admin)
    return new_admin


async def create_session(async_session: async_sessionmaker[AsyncSession], 
                         session_string: str, password: bytes, name:str) -> Session:
    async with async_session() as session:
        res = await session.execute(
            select(Session).
            where(Session.session_string == session_string))
        
        existing_session = res.scalar_one_or_none()
        if existing_session is not None:
            return existing_session

        new_session = Session(session_string=session_string, password=password, name=name)
        session.add(new_session)
        await session.commit()
        await session.refresh(new_session)
    return new_session


async def create_groups(async_session: async_sessionmaker[AsyncSession], 
                        groups: list[tuple[int, str, datetime, str]], session_id: int):
    async with async_session() as session:
        for g in groups:
            existing_group = await session.get(Group, g[0])
            if existing_group is not None:
                continue

            new_group = Group(id=g[0], name=g[1], created_at=g[2], link=g[3], session_id=session_id)
            session.add(new_group)
            await session.commit()


async def create_price(async_session: async_sessionmaker[AsyncSession], 
                       age: int, price: float) -> Price:
    async with async_session() as session:
        res = await session.execute(
            select(Price).
            where(Price.age == age))
        
        existing_price = res.scalar_one_or_none()
        if existing_price is not None:
            return existing_price
        
        new_price = Price(age=age, price=price)
        session.add(new_price)
        await session.commit()
        await session.refresh(new_price)
    return new_price
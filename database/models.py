from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())


class Session(Base):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    session_string: Mapped[str] = mapped_column()
    password: Mapped[bytes] = mapped_column()


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
    buyer_id: Mapped[int] = mapped_column(nullable=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('sessions.id'))
    created_at: Mapped[datetime] = mapped_column()


class Price(Base):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    
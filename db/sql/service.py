import datetime
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, literal_column, update, delete

from db.sql.connect import AsyncSessionMaker
from db.sql.models import Users


class SqlService(ABC):
    @abstractmethod
    async def run(self):
        raise NotImplementedError


class ReadUser(SqlService):

    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            user = await session.scalar(select(Users).where(Users.tg_id == literal_column(str(self.tg_id))))
            return user


class CreateUser(SqlService):
    def __init__(self, tg_id: int, username: Optional[str] = None, click: int = 0):
        self.tg_id = tg_id
        self.username = username
        self.click = click

    async def run(self):
        async with AsyncSessionMaker() as session:
            new_user = Users(tg_id=self.tg_id)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user


class UpdateUser(SqlService):
    def __init__(self, tg_id: int, date_time: Optional[datetime.datetime] = None):
        self.tg_id = tg_id
        self.date_time = date_time

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(Users)
                .where(Users.tg_id == literal_column(str(self.tg_id)))
                .values(
                    expired_date=self.date_time if self.date_time is not None else Users.expired_date,
                )
            )
            await session.execute(stmt)
            await session.commit()


class DeleteUser(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = delete(Users).where(Users.tg_id == literal_column(str(self.tg_id)))
            await session.execute(stmt)
            await session.commit()


class AllUsers(SqlService):
    async def run(self):
        async with AsyncSessionMaker() as session:
            users_scalar = await session.scalars(select(Users))
            return users_scalar.all()


async def run_sql(runnable: SqlService):
    return await runnable.run()

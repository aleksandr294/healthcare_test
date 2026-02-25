import typing
import uuid

import fastapi
import sqlalchemy as sa
from sqlalchemy.ext import asyncio as sa_asyncio

from components.core import database


class BaseRepository:
    def __init__(self, model: typing.Type[database.Base]) -> None:
        self.model = model

    async def get_all(self, conn: sa_asyncio.AsyncSession) -> typing.List[database.Base]:
        query = sa.select(self.model)
        result = await conn.execute(query)

        instances = result.scalars().all()
        return instances

    async def get_by_id(self, id: int, conn: sa_asyncio.AsyncSession) -> database.Base:
        query = sa.select(self.model).where(self.model.id == id)
        result = await conn.execute(query)

        instance = result.scalar_one_or_none()
        return instance

    async def get_by_ids(self, ids: typing.List[int], conn: sa_asyncio.AsyncSession) -> typing.List[database.Base]:
        query = sa.select(self.model).where(self.model.id.in_(ids))
        result = await conn.execute(query)

        instances = result.scalars().all()
        return instances

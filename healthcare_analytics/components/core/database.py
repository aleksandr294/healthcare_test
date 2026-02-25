import contextlib
import typing

import fastapi
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from components.core import config

Base = orm.declarative_base()
SessionMaker = typing.Callable[[], typing.AsyncContextManager[AsyncSession]]
cnfg = config.get_config()


class DatabaseMngr:
    def __init__(self, engine: typing.Optional[AsyncEngine] = None) -> None:
        self.engine = engine

    def get_session(self) -> sessionmaker:
        return sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def connect(self) -> typing.Any:
        session_maker = self.get_session()
        async with session_maker() as conn:
            yield conn

    instance: typing.Optional[typing.Any] = None

    @staticmethod
    def get_db() -> "DatabaseMngr":
        if not DatabaseMngr.instance:
            engine = create_async_engine(
                cnfg.POSTGRES_URL.unicode_string(),
                echo=False,
                future=True,
                pool_size=100,
                max_overflow=200,
            )
            DatabaseMngr.instance = DatabaseMngr(engine)

        return typing.cast(DatabaseMngr, DatabaseMngr.instance)


async def get_session(
    db: DatabaseMngr = fastapi.Depends(DatabaseMngr.get_db),
) -> AsyncSession:
    async with db.connect() as conn:
        yield conn

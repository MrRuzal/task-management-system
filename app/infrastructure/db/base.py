from asyncio import current_task
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)
from sqlalchemy.orm import declarative_base, declared_attr


class Database:
    def __init__(self, db_url: str, pool_size: int = 5) -> None:
        self.db_url = db_url
        self._async_engine = create_async_engine(
            self.db_url,
            pool_pre_ping=True,
            pool_size=pool_size,
        )
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                self._async_engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )

    def get_session(self) -> AsyncSession:
        return self._session_factory()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class CustomBase:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


metadata = MetaData()
Base = declarative_base(cls=CustomBase, metadata=metadata)

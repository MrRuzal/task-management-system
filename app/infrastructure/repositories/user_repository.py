from typing import Callable, AsyncContextManager
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.db.models.user import (
    UserModel,
)


class SQLAlchemyUserRepository(UserRepository):
    session_contextmanager: Callable[
        ..., AsyncContextManager[AsyncSession]
    ] = None

    def __init__(
        self,
        session_contextmanager: Callable[
            ..., AsyncContextManager[AsyncSession]
        ],
    ):
        super().__init__()
        self.session_contextmanager = session_contextmanager

    async def create(self, user: User) -> User:
        """
        Создать нового пользователя.

        :param user: объект пользователя для создания
        :return: созданный пользователь с присвоенным id
        :raises ValueError: если email или username уже существуют
        """
        async with self.session_contextmanager() as session:
            db_user = UserModel.from_entity(user)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user.to_entity()

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Получить пользователя по его идентификатору.

        :param user_id: идентификатор пользователя
        :return: найденный пользователь или None
        """
        async with self.session_contextmanager() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            db_user = result.scalar_one_or_none()
            return db_user.to_entity() if db_user else None

    async def get_by_email(self, email: str) -> User | None:
        """
        Получить пользователя по его email.

        :param email: email пользователя
        :return: найденный пользователь или None
        """
        async with self.session_contextmanager() as session:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await session.execute(stmt)
            user_row = result.scalar_one_or_none()
            if user_row:
                return user_row.to_entity()
            return None

    async def get_by_username(self, username: str) -> User | None:
        """
        Получить пользователя по его имени пользователя.

        :param username: имя пользователя
        :return: найденный пользователь или None
        """
        async with self.session_contextmanager() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            db_user = result.scalar_one_or_none()
            return db_user.to_entity() if db_user else None

    async def delete(self, user_id: int) -> None:
        """
        Удалить пользователя по его идентификатору.

        :param user_id: идентификатор пользователя
        """
        async with self.session_contextmanager() as session:
            await session.execute(
                delete(UserModel).where(UserModel.id == user_id)
            )
            await session.commit()

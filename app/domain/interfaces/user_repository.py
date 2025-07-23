from abc import ABC, abstractmethod
from app.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Создать нового пользователя.

        :param user: объект пользователя для создания
        :return: созданный пользователь с присвоенным id
        :raises ValueError: если email или username уже существуют
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """
        Получить пользователя по его идентификатору.

        :param user_id: идентификатор пользователя
        :return: найденный пользователь или None
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """
        Получить пользователя по его email.

        :param email: email пользователя
        :return: найденный пользователь или None
        """
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """
        Получить пользователя по его имени пользователя.

        :param username: имя пользователя
        :return: найденный пользователь или None
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """
        Удалить пользователя по его идентификатору.

        :param user_id: идентификатор пользователя
        """
        pass

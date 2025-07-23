from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepository
from app.application.use_cases.user import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    GetUserByUsernameUseCase,
    DeleteUserUseCase,
)


class UserService:
    """
    Сервис для управления пользователями.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Инициализация сервиса с внедрением зависимостей.

        :param user_repository: Репозиторий пользователей
        """
        self.create_user_uc = CreateUserUseCase(user_repository)
        self.get_user_by_id_uc = GetUserByIdUseCase(user_repository)
        self.get_user_by_username_uc = GetUserByUsernameUseCase(
            user_repository
        )
        self.delete_user_uc = DeleteUserUseCase(user_repository)

    async def create_user(self, user: User) -> User:
        """
        Создать нового пользователя.
        :param user: Данные пользователя для создания
        :return: Созданный пользователь
        """
        return await self.create_user_uc.execute(user)

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получить пользователя по его ID.
        :param user_id: ID пользователя
        :return: Пользователь или None, если не найден
        """
        return await self.get_user_by_id_uc.execute(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Получить пользователя по его имени пользователя.
        :param username: Имя пользователя
        :return: Пользователь или None, если не найден
        """
        return await self.get_user_by_username_uc.execute(username)

    async def delete_user(self, user_id: int) -> None:
        """
        Удалить пользователя по его ID.
        """
        await self.delete_user_uc.execute(user_id)

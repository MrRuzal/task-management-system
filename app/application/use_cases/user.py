from passlib.context import CryptContext
from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepository
from app.entrypoints.api.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_create: UserCreate) -> User:
        """
        Создать нового пользователя.

        :param user_create: данные пользователя для создания
        :return: созданный пользователь с id
        :raises ValueError: если username пустой или уже существует, или email уже зарегистрирован
        """
        if not user_create.username.strip():
            raise ValueError("Username cannot be empty")

        existing_user = await self.user_repository.get_by_username(
            user_create.username
        )
        if existing_user:
            raise ValueError("Username already exists")

        existing_email = await self.user_repository.get_by_email(
            user_create.email
        )
        if existing_email:
            raise ValueError("Email already registered")

        hashed_password = pwd_context.hash(user_create.password)

        user_entity = User(
            id=None,
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            is_active=True,
        )

        return await self.user_repository.create(user_entity)


class GetUserByIdUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> User | None:
        """
        Получить пользователя по ID.

        :param user_id: ID пользователя
        :return: найденный пользователь или None
        """
        return await self.repository.get_by_id(user_id)


class GetUserByUsernameUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, username: str) -> User | None:
        """
        Получить пользователя по username.

        :param username: уникальное имя пользователя
        :return: найденный пользователь или None
        """
        return await self.repository.get_by_username(username)


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> None:
        """
        Удалить пользователя по ID.

        :param user_id: ID пользователя
        """
        await self.repository.delete(user_id)

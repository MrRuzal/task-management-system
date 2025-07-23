from dependency_injector import containers, providers

from app.infrastructure.db.base import Database
from app.config import settings
from app.infrastructure.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from app.application.services.user_service import UserService
from app.application.use_cases.user import CreateUserUseCase
from app.infrastructure.repositories.task_repository import (
    SQLAlchemyTaskRepository,
)
from app.application.services.task_service import TaskService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        packages=["app.entrypoints.api.routes"]
    )

    db = providers.Singleton(Database, db_url=settings.DATABASE_URL)

    session_contextmanager = providers.Factory(db.provided.session)

    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session_contextmanager=session_contextmanager,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
    )

    task_repository = providers.Factory(
        SQLAlchemyTaskRepository,
        session_contextmanager=session_contextmanager,
    )

    task_service = providers.Factory(
        TaskService,
        task_repository=task_repository,
    )

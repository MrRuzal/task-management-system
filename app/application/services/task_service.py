from app.domain.entities.task import Task
from app.entrypoints.api.schemas.task import TaskCreate, TaskUpdate
from app.domain.interfaces.task_repository import TaskRepository
from app.application.use_cases.task import (
    CreateTaskUseCase,
    GetTaskByIdUseCase,
    GetAllTasksUseCase,
    GetAllTasksByUserIdUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
)


class TaskService:
    """
    Сервис для управления задачами.
    """

    def __init__(self, task_repository: TaskRepository):
        """
        Инициализация сервиса с внедрением зависимостей.

        :param task_repository: Репозиторий задач
        """
        self.create_task_uc = CreateTaskUseCase(task_repository)
        self.get_task_by_id_uc = GetTaskByIdUseCase(task_repository)
        self.get_all_tasks_uc = GetAllTasksUseCase(task_repository)
        self.get_all_tasks_by_user_id_uc = GetAllTasksByUserIdUseCase(
            task_repository
        )
        self.update_task_uc = UpdateTaskUseCase(task_repository)
        self.delete_task_uc = DeleteTaskUseCase(task_repository)

    async def create_task(self, task_create: TaskCreate, user_id: int) -> Task:
        """
        Создать новую задачу.

        :param task_create: Данные для создания задачи
        :param user_id: ID пользователя, которому принадлежит задача
        :return: Созданная задача
        """
        task_entity = Task(
            id=None,
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
            user_id=user_id,
        )
        return await self.create_task_uc.execute(task_entity)

    async def update_task(
        self, task_update: TaskUpdate, task_id: int, user_id: int
    ) -> Task:
        """
        Обновить существующую задачу.

        :param task_update: Данные для обновления задачи
        :param task_id: ID задачи
        :param user_id: ID пользователя, которому принадлежит задача
        :return: Обновленная задача
        """
        task_entity = Task(
            id=task_id,
            title=task_update.title,
            description=task_update.description,
            due_date=task_update.due_date,
            user_id=user_id,
        )
        return await self.update_task_uc.execute(task_entity)

    async def get_task_by_id(self, task_id: int) -> Task | None:
        """
        Получить задачу по её ID.

        :param task_id: ID задачи
        :return: Задача или None, если не найдена
        """
        return await self.get_task_by_id_uc.execute(task_id)

    async def get_all_tasks(self) -> list[Task]:
        """
        Получить список всех задач.

        :return: Список задач
        """
        return await self.get_all_tasks_uc.execute()

    async def get_all_tasks_by_user_id(self, user_id: int) -> list[Task]:
        """
        Получить задачи, принадлежащие конкретному пользователю.

        :param user_id: ID пользователя
        :return: Список задач пользователя
        """
        return await self.get_all_tasks_by_user_id_uc.execute(user_id)

    async def delete_task(self, task_id: int) -> None:
        """
        Удалить задачу по её ID.

        :param task_id: ID задачи
        """
        await self.delete_task_uc.execute(task_id)

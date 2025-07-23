from app.domain.entities.task import Task
from app.domain.interfaces.task_repository import TaskRepository


class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def execute(self, task: Task) -> Task:
        """
        Создать новую задачу.

        :param task: объект задачи для создания
        :return: созданная задача с присвоенным id
        :raises ValueError: если title пустой
        """
        if not task.title.strip():
            raise ValueError("Title cannot be empty")
        return await self.repository.create(task)


class GetTaskByIdUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def execute(self, task_id: int) -> Task | None:
        """
        Получить задачу по её идентификатору.

        :param task_id: ID задачи
        :return: найденная задача или None
        """
        return await self.repository.get_by_id(task_id)


class GetAllTasksUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def execute(self) -> list[Task]:
        """
        Получить список всех задач.

        :return: список всех задач
        """
        return await self.repository.get_all()


class GetAllTasksByUserIdUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> list[Task]:
        """
        Получить все задачи пользователя.

        :param user_id: ID пользователя
        :return: задачи пользователя
        """
        return await self.repository.get_all_by_user_id(user_id)


class UpdateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def execute(self, task: Task) -> Task:
        """
        Обновить задачу.

        :param task: обновлённый объект задачи
        :return: обновлённая задача
        :raises ValueError: если title пустой
        """
        if not task.title.strip():
            raise ValueError("Title cannot be empty")
        return await self.repository.update(task)


class DeleteTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def execute(self, task_id: int) -> None:
        """
        Удалить задачу по ID.

        :param task_id: ID задачи
        """
        await self.repository.delete(task_id)

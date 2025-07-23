from abc import ABC, abstractmethod
from app.domain.entities.task import Task


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: Task) -> Task:
        """
        Создать новую задачу.

        :param task: объект задачи для создания
        :return: созданная задача с присвоенным id
        :raises ValueError: если title пустой
        """
        pass

    @abstractmethod
    async def get_by_id(self, task_id: int) -> Task | None:
        """
        Получить задачу по её идентификатору.

        :param task_id: идентификатор задачи
        :return: найденная задача или None
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Task]:
        """
        Получить все задачи.

        :return: список всех задач
        """
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[Task]:
        """
        Получить все задачи по идентификатору пользователя.

        :param user_id: идентификатор пользователя
        :return: список задач пользователя
        """
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        """
        Обновить задачу.

        :param task: объект задачи с обновленными данными
        :return: обновленная задача
        :raises ValueError: если задача не найдена
        """
        pass

    @abstractmethod
    async def delete(self, task_id: int) -> None:
        """
        Удалить задачу по её идентификатору.

        :param task_id: идентификатор задачи
        """
        pass

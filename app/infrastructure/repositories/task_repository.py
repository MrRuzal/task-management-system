from typing import Callable, AsyncContextManager
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.task import Task
from app.domain.interfaces.task_repository import TaskRepository
from app.infrastructure.db.models.task import TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    session_contextmanager: Callable[
        ..., AsyncContextManager[AsyncSession]
    ] = None

    def __init__(
        self,
        session_contextmanager: Callable[
            ..., AsyncContextManager[AsyncSession]
        ],
    ):
        self.session_contextmanager = session_contextmanager

    async def create(self, task: Task) -> Task:
        """
        Создать новую задачу.

        :param task: объект задачи для создания
        :return: созданная задача с присвоенным id
        :raises ValueError: если title пустой
        """
        async with self.session_contextmanager() as session:
            db_task = TaskModel(
                title=task.title,
                description=task.description,
                due_date=task.due_date,
                user_id=task.user_id,
            )
            session.add(db_task)
            await session.commit()
            await session.refresh(db_task)
            return Task(
                id=db_task.id,
                title=db_task.title,
                description=db_task.description,
                due_date=db_task.due_date,
                user_id=db_task.user_id,
            )

    async def get_by_id(self, task_id: int) -> Task | None:
        """
        Получить задачу по её идентификатору.

        :param task_id: идентификатор задачи
        :return: найденная задача или None
        """
        async with self.session_contextmanager() as session:
            result = await session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            )
            db_task = result.scalar_one_or_none()
            if db_task is None:
                return None
            return Task(
                id=db_task.id,
                title=db_task.title,
                description=db_task.description,
                due_date=db_task.due_date,
                user_id=db_task.user_id,
            )

    async def get_all(self) -> list[Task]:
        """
        Получить все задачи.

        :return: список всех задач
        """
        async with self.session_contextmanager() as session:
            result = await session.execute(select(TaskModel))
            db_tasks = result.scalars().all()
            return [
                Task(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    due_date=t.due_date,
                    user_id=t.user_id,
                )
                for t in db_tasks
            ]

    async def get_all_by_user_id(self, user_id: int) -> list[Task]:
        """
        Получить все задачи по идентификатору пользователя.

        :param user_id: идентификатор пользователя
        :return: список задач пользователя
        """
        async with self.session_contextmanager() as session:
            result = await session.execute(
                select(TaskModel).where(TaskModel.user_id == user_id)
            )
            db_tasks = result.scalars().all()
            return [
                Task(
                    id=t.id,
                    title=t.title,
                    description=t.description,
                    due_date=t.due_date,
                    user_id=t.user_id,
                )
                for t in db_tasks
            ]

    async def update(self, task: Task) -> Task:
        """
        Обновить задачу.

        :param task: объект задачи с обновленными данными
        :return: обновленная задача
        :raises ValueError: если задача не найдена
        """
        async with self.session_contextmanager() as session:
            await session.execute(
                update(TaskModel)
                .where(TaskModel.id == task.id)
                .values(
                    title=task.title,
                    description=task.description,
                    due_date=task.due_date,
                    user_id=task.user_id,
                )
            )
            await session.commit()
            return await self.get_by_id(task.id)

    async def delete(self, task_id: int) -> None:
        """
        Удалить задачу по её идентификатору.

        :param task_id: идентификатор задачи
        """
        async with self.session_contextmanager() as session:
            await session.execute(
                delete(TaskModel).where(TaskModel.id == task_id)
            )
            await session.commit()

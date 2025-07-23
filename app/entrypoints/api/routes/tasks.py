from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.task_service import TaskService
from app.entrypoints.api.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.container import Container
from app.entrypoints.api.dependencies import get_current_user
from app.domain.entities.user import User
from app.entrypoints.api.schemas.user import UserRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service():
    return Container.task_service()


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    task_service=Depends(get_task_service),
    current_user: UserRead = Depends(get_current_user),
):
    created_task = await task_service.create_task(task_create, current_user.id)
    return TaskRead.model_validate(created_task)


@router.get("/", response_model=list[TaskRead])
async def get_all_tasks(
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.get_all_tasks()


@router.get("/user", response_model=list[TaskRead])
async def get_tasks_by_user(
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.get_all_tasks_by_user_id(current_user.id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    task = await task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    task_service=Depends(get_task_service),
):
    updated_task = await task_service.update_task(
        task_update, task_id, current_user.id
    )
    return TaskRead.model_validate(updated_task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    await task_service.delete_task(task_id)

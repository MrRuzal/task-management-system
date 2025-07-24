import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.task_service import TaskService
from app.entrypoints.api.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.container import Container
from app.entrypoints.api.dependencies import get_current_user
from app.domain.entities.user import User
from app.entrypoints.api.schemas.user import UserRead
from app.common.logs import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service():
    return Container.task_service()


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    task_service=Depends(get_task_service),
    current_user: UserRead = Depends(get_current_user),
):
    try:
        created_task = await task_service.create_task(
            task_create, current_user.id
        )
        return TaskRead.model_validate(created_task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(status_code=409, detail="Task already exists")
    except Exception as e:
        logger.error(f"Unexpected error in create_task: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=list[TaskRead], status_code=status.HTTP_200_OK)
async def get_all_tasks(
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    try:
        return await task_service.get_all_tasks()
    except Exception as e:
        logger.error(f"Error in get_all_tasks: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/user", response_model=list[TaskRead], status_code=status.HTTP_200_OK
)
async def get_tasks_by_user(
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    try:
        return await task_service.get_all_tasks_by_user_id(current_user.id)
    except Exception as e:
        logger.error(f"Error in get_tasks_by_user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK
)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    try:
        task = await task_service.get_task_by_id(task_id)
        if task is None:
            logger.error(f"Task not found: task_id={task_id}")
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_task: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put(
    "/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK
)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    task_service=Depends(get_task_service),
):
    try:
        updated_task = await task_service.update_task(
            task_update, task_id, current_user.id
        )
        return TaskRead.model_validate(updated_task)
    except ValueError as e:
        logger.error(f"Validation error in update_task: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except sqlalchemy.exc.NoResultFound:
        logger.error(f"Task not found in update_task: task_id={task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        logger.error(f"Unexpected error in update_task: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
):
    try:
        await task_service.delete_task(task_id)
    except sqlalchemy.exc.NoResultFound:
        logger.error(f"Task not found in delete_task: task_id={task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        logger.error(f"Error in delete_task: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

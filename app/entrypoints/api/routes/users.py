from fastapi import APIRouter, Depends, HTTPException, status

from app.entrypoints.api.schemas.user import UserCreate, UserRead
from app.entrypoints.api.dependencies import get_user_service
from app.common.logs import logger

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    user_service=Depends(get_user_service),
):
    try:
        user = await user_service.create_user(user_create)
        return UserRead.model_validate(user)
    except ValueError as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail="Invalid user data")


@router.get(
    "/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: int,
    user_service=Depends(get_user_service),
):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return user

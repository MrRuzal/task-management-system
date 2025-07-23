from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.entrypoints.api.schemas.user import UserCreate, UserRead
from app.entrypoints.api.dependencies import get_user_service

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
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service=Depends(get_user_service),
):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

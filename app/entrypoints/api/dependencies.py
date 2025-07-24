from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.container import Container
from app.infrastructure.security import decode_access_token
from app.domain.entities.user import User
from app.application.services.user_service import UserService
from app.common.logs import logger
from app.entrypoints.api.schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@inject
async def get_async_session(
    session: AsyncSession = Depends(Provide[Container.session_contextmanager]),
) -> AsyncSession:
    async with session() as s:
        yield s


def get_user_service(request: Request):
    return request.app.container.user_service()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = await user_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return UserRead.model_validate(user)


def get_task_service(request: Request):
    return request.app.container.task_service()


def make_naive(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

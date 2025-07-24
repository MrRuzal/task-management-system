from dependency_injector.wiring import inject, Provide
from app.container import Container
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.infrastructure.security import verify_password, create_access_token
from app.domain.entities.user import User
from app.common.logs import logger

router = APIRouter()


@router.post("/login", response_model=None, status_code=status.HTTP_200_OK)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service=Depends(Provide[Container.user_service]),
):
    try:
        user: User | None = await user_service.get_user_by_username(
            form_data.username
        )
        if not user or not verify_password(
            form_data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        logger.warning(f"Login failed: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

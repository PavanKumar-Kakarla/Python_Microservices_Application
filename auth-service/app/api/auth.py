from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
    RefreshTokenRequest,
    AccessTokenResponse
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix= "/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return AuthService.register_user(
            db=db,
            user_data=user
        )
    
    except Exception:
        raise


@router.post(
    "/login",
    response_model=Token,
    status_code=200
)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    return AuthService.login_user(
        db=db,
        user_data=user
    )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.post(
    "/refresh",
    response_model=AccessTokenResponse
)
def refresh_access_token(
    refresh_data: RefreshTokenRequest
):
    return AuthService.refresh_access_token(
        refresh_data
    )
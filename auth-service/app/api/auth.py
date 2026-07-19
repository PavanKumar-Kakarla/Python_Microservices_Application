from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
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
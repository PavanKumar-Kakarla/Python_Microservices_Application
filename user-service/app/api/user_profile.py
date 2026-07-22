from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import validate_access_token
from app.schemas.user_profile_schema import (
    UserProfileCreate,
    UserProfileResponse,
    UserProfileUpdate
)
from app.services.user_profile_service import UserProfileService
from app.schemas.auth_schema import ValidateTokenResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserProfileResponse,
    status_code=201
)
def create_user_profile(
    user: UserProfileCreate,
    db: Session = Depends(get_db)
):
    return UserProfileService.create_user_profile(
        db=db,
        user_data=user
    )


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse
)
def get_user_profile(
    user_id: int,
    current_user: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return UserProfileService.get_user_profile(
        db=db,
        user_id=user_id
    )


@router.put(
    "/{user_id}",
    response_model=UserProfileResponse
)
def update_user_profile(
    user_id: int,
    user: UserProfileUpdate,
    current_user: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return UserProfileService.update_user_profile(
        db=db,
        user_id=user_id,
        user_data=user
    )


@router.delete(
    "/{user_id}",
    status_code=204
)
def delete_user_profile(
    user_id: int,
    current_user: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    UserProfileService.delete_user_profile(
        db=db,
        user_id=user_id
    )

    return Response(status_code=204)
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate


class AuthService:

    @staticmethod
    def register_user(
        db:Session,
        user_data: UserCreate
    ) -> User:
        try:
            existing_user = UserRepository.get_user_by_email(
                db=db,
                email=user_data.email
            )

            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail="User already exists"
                )
            
            user = User(
                email=user_data.email,
                password_hash=hash_password(user_data.password)
            )

            created_user = UserRepository.create_user(
                db=db,
                user=user
            )

            return created_user
        
        except Exception:
            raise
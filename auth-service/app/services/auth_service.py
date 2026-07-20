from sqlalchemy.orm import Session

from app.core.security import hash_password, create_access_token, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserLogin, Token
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException
)


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
                raise UserAlreadyExistsException()
            
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

    
    @staticmethod
    def login_user(
        db: Session,
        user_data: UserLogin
    ) -> Token:
        try:

            user = UserRepository.get_user_by_email(
                db=db,
                email=user_data.email
            )

            if not user:
                raise InvalidCredentialsException()
            
            if not verify_password(
                user_data.password,
                user.password_hash
            ):
                raise InvalidCredentialsException()
            
            access_token = create_access_token(
                data={
                    "sub": user.email
                }
            )

            return Token(
                access_token=access_token,
                token_type="Bearer"
            )
        
        except Exception:
            raise

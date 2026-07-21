from sqlalchemy.orm import Session

from app.core.security import hash_password, create_access_token, verify_password, create_refresh_token, decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserLogin, Token, AccessTokenResponse, RefreshTokenRequest
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InvalidRefreshTokenException
)
from app.core.logger import logger


class AuthService:

    @staticmethod
    def register_user(
        db:Session,
        user_data: UserCreate
    ) -> User:
        try:
            logger.info(
                "Register request received for email: %s",
                user_data.email
            )

            existing_user = UserRepository.get_user_by_email(
                db=db,
                email=user_data.email
            )

            if existing_user:

                logger.warning(
                    "Registration failed. User already exists: %s",
                    user_data.email
                )
                raise UserAlreadyExistsException()
            
            user = User(
                email=user_data.email,
                password_hash=hash_password(user_data.password)
            )

            created_user = UserRepository.create_user(
                db=db,
                user=user
            )

            logger.info(
                "User registered successfully: %s",
                created_user.email
            )

            return created_user
        
        except (
            UserAlreadyExistsException,
            InvalidCredentialsException
        ):
            raise
        
        except Exception:
            logger.exception("Unexpected error during user registration.")
            raise

    
    @staticmethod
    def login_user(
        db: Session,
        user_data: UserLogin
    ) -> Token:
        try:

            logger.info(
                "Login request received for email: %s",
                user_data.email
            )

            user = UserRepository.get_user_by_email(
                db=db,
                email=user_data.email
            )

            if not user:

                logger.warning(
                    "Login failed for email: %s",
                    user_data.email
                )

                raise InvalidCredentialsException()
            
            if not verify_password(
                user_data.password,
                user.password_hash
            ):
                
                logger.warning(
                    "Login failed for email: %s",
                    user_data.email
                )

                raise InvalidCredentialsException()
            
            access_token = create_access_token(
                data={
                    "sub": user.email
                }
            )

            refresh_token = create_refresh_token(
                data={
                    "sub": user.email
                }
            )

            logger.info(
                "Login successful for email: %s",
                user.email
            )

            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer"
            )
        
        except InvalidCredentialsException:
            raise

        except Exception:
            logger.exception("Unexpected error during login.")
            raise

    
    @staticmethod
    def refresh_access_token(
        refresh_data: RefreshTokenRequest
    ) -> AccessTokenResponse:
        
        try:
            payload = decode_access_token(
                refresh_data.refresh_token
            )

            if payload.get("type") != "refresh":
                raise InvalidRefreshTokenException()
            
            email = payload.get("sub")
            if email is None:
                raise InvalidCredentialsException()
            
            access_token = create_access_token(
                data={
                    "sub": email
                }
            )

            logger.info(
                "Access token refreshed successfully for email: %s",
                email
            )

            return AccessTokenResponse(
                access_token=access_token,
                token_type="Bearer"
            )
        
        except InvalidRefreshTokenException:
            raise
        
        except InvalidCredentialsException:
            raise

        except Exception:
            logger.exception(
                "Unexpected error while refreshing access token."
            )
            raise
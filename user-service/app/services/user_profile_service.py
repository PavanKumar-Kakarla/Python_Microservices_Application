from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile
from app.repositories.user_profile_repository import UserProfileRepository
from app.schemas.user_profile_schema import (
    UserProfileCreate,
    UserProfileUpdate
)
from app.core.logger import logger
from app.core.exceptions import UserAlreadyExistsException, UserNotFoundException


class UserProfileService:

    @staticmethod
    def create_user_profile(
        db: Session,
        user_data: UserProfileCreate
    ) -> UserProfile:
        
        try:

            logger.info(
                "Create profile request received for email: %s",
                user_data.email
            )

            existing_user = UserProfileRepository.get_user_by_email(
                db=db,
                email=user_data.email
            )

            if existing_user:
                logger.warning(
                    "Profile already exists: %s",
                    user_data.email
                )
                raise UserAlreadyExistsException()

            profile = UserProfile(
                email=user_data.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone=user_data.phone
            )

            created_profile = (
                UserProfileRepository.create_user_profile(
                    db=db,
                    user_profile=profile
                )
            )

            logger.info(
                "Profile created successfully: %s",
                created_profile.email
            )

            return created_profile
        
        except UserAlreadyExistsException:
            raise

        except Exception:
            logger.exception(
                "Unexpected error while creating user profile."
            )
            raise


    @staticmethod
    def get_user_profile(
        db: Session,
        user_id: int
    ) -> UserProfile:
        
        try:

            logger.info(
                "Fetching profile with id: %s",
                user_id
            )

            user = UserProfileRepository.get_user_by_id(
                db=db,
                user_id=user_id
            )

            if not user:

                logger.warning(
                    "User profile not found: %s",
                    user_id
                )

                raise UserNotFoundException()
            
            return user
        
        except UserNotFoundException:
            raise

        except Exception:
            logger.exception(
                "Unexpected error while fetching user profile."
            )
            raise


    
    @staticmethod
    def update_user_profile(
        db: Session,
        user_id: int,
        user_data: UserProfileUpdate
    ) -> UserProfile:

        try:

            logger.info(
                "Update profile request received for id: %s",
                user_id
            )

            user = UserProfileRepository.get_user_by_id(
                db=db,
                user_id=user_id
            )

            if not user:

                logger.warning(
                    "User profile not found: %s",
                    user_id
                )

                raise UserNotFoundException()

            if user_data.first_name is not None:
                user.first_name = user_data.first_name

            if user_data.last_name is not None:
                user.last_name = user_data.last_name

            if user_data.phone is not None:
                user.phone = user_data.phone

            updated_user = (
                UserProfileRepository.update_user_profile(
                    db=db,
                    user_profile=user
                )
            )

            logger.info(
                "Profile updated successfully: %s",
                updated_user.email
            )

            return updated_user

        except UserNotFoundException:
            raise

        except Exception:
            logger.exception(
                "Unexpected error while updating profile."
            )
            raise


    @staticmethod
    def delete_user_profile(
        db: Session,
        user_id: int
    ) -> None:

        try:

            logger.info(
                "Delete profile request received for id: %s",
                user_id
            )

            user = UserProfileRepository.get_user_by_id(
                db=db,
                user_id=user_id
            )

            if not user:

                logger.warning(
                    "User profile not found: %s",
                    user_id
                )

                raise UserNotFoundException()

            UserProfileRepository.delete_user_profile(
                db=db,
                user_profile=user
            )

            logger.info(
                "Profile deleted successfully: %s",
                user.email
            )

        except UserNotFoundException:
            raise

        except Exception:
            logger.exception(
                "Unexpected error while deleting profile."
            )
            raise


    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ):

        user = UserProfileRepository.get_user_by_email(
            db,
            email
        )

        if not user:
            raise UserNotFoundException()

        return user
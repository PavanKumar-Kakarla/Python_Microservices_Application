from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile


class UserProfileRepository:

    @staticmethod
    def create_user_profile(
        db: Session,
        user_profile: UserProfile
    ) -> UserProfile:
        
        try:
            db.add(user_profile)
            db.commit()
            db.refresh(user_profile)


            return user_profile
        
        except Exception:
            db.rollback()
            raise

    
    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ) -> UserProfile | None:
        
        return (
            db.query(UserProfile)
            .filter(UserProfile.email == email)
            .first()
        )
    

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: int
    ) -> UserProfile | None:
        
        return (
            db.query(UserProfile)
            .filter(UserProfile.id == user_id)
            .first()
        )
    

    @staticmethod
    def update_user_profile(
        db: Session,
        user_profile: UserProfile
    ) -> UserProfile:
        
        try:
            db.commit()
            db.refresh(user_profile)

            return user_profile
        
        except Exception:
            db.rollback()
            raise


    @staticmethod
    def delete_user_profile(
        db: Session,
        user_profile: UserProfile
    ) -> None:

        try:
            db.delete(user_profile)
            db.commit()

        except Exception:
            db.rollback()
            raise

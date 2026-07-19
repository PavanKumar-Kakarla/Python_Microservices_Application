from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def create_user(db: Session, user: User) -> User:
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        
        except Exception:
            db.rollback()
            raise


    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        try:
            return (
                db.query(User)
                .filter(User.email == email)
                .first()
            )
        
        except Exception:
            raise

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        try:
            return (
                db.query(User)
                .filter(User.id == user_id)
                .first()
            )
        
        except Exception:
            raise

    @staticmethod
    def update_user(db: Session, user: User) -> User:
        try:
            db.commit()
            db.refresh(user)
            return user
        
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        try:
            db.delete(user)
            db.commit()

        except Exception:
            db.rollback()
            raise
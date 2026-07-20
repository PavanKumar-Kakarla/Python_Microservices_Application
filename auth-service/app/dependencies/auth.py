from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.core.exceptions import UserNotFoundException
from app.dependencies.database import get_db
from app.repositories.user_repository import UserRepository


security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = decode_access_token(token)

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )
    
    user = UserRepository.get_user_by_email(
        db=db,
        email=email
    )

    if user is None:
        raise UserNotFoundException()
    
    return user
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.clients.auth_client import AuthClient


security = HTTPBearer()


def validate_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    access_token = credentials.credentials

    result = AuthClient.validate_token(access_token)

    if not result.valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    return result
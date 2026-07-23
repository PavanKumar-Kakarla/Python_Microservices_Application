from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.gateway_service import GatewayService

router = APIRouter(
    prefix="/gateway",
    tags=["Gateway"]
)

security = HTTPBearer()


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return GatewayService.get_user(
        user_id=user_id,
        headers={
            "Authorization": f"Bearer {credentials.credentials}"
        }
    )
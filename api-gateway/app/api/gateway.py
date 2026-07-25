from fastapi import APIRouter, Depends, Response
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


@router.post("/users", status_code=201)
def create_user(
    user: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return GatewayService.create_user(
        data=user,
        headers={
            "Authorization": f"Bearer {credentials.credentials}"
        }
    )


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return GatewayService.update_user(
        user_id=user_id,
        data=user,
        headers={
            "Authorization": f"Bearer {credentials.credentials}"
        }
    )


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    GatewayService.delete_user(
        user_id=user_id,
        headers={
            "Authorization": f"Bearer {credentials.credentials}"
        }
    )

    return Response(status_code=204)
from fastapi import APIRouter, Request, Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.gateway_service import GatewayService


router = APIRouter(
    prefix="/gateway/orders",
    tags=["Orders"]
)


security = HTTPBearer()


def get_headers(request: Request):

    authorization = request.headers.get("Authorization")

    headers = {}

    if authorization:
        headers["Authorization"] = authorization

    return headers


@router.get("")
def get_orders(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    headers = get_headers(request)

    return GatewayService.get_orders(headers)


@router.post("")
def create_order(
    request: Request,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    headers = get_headers(request)

    headers["Idempotency-Key"] = idempotency_key

    return GatewayService.create_order(headers)


@router.get("/{order_id}")
def get_order(
    order_id: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    headers = get_headers(request)

    return GatewayService.get_order(
        order_id,
        headers
    )


@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    request: Request,
    status: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    headers = get_headers(request)

    return GatewayService.update_order_status(
        order_id,
        status,
        headers
    )
from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.gateway_service import GatewayService


router = APIRouter(
    prefix="/gateway/payments",
    tags=["Payments"]
)

security = HTTPBearer()

def get_headers(request: Request):

    authorization = request.headers.get("Authorization")

    headers = {}

    if authorization:
        headers["Authorization"] = authorization

    return headers


@router.post("", status_code=status.HTTP_201_CREATED)
def create_payment(
    data: dict,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    headers = get_headers(request)

    return GatewayService.create_payment(
        data=data,
        headers=headers
    )


@router.get("/{payment_id}")
def get_payment(
    payment_id: int, 
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    headers = get_headers(request)

    return GatewayService.get_payment(
        payment_id=payment_id,
        headers=headers
    )


@router.get("/order/{order_id}")
def get_payment(order_id: int, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):

    headers = get_headers(request)

    return GatewayService.get_payment_by_order(
        order_id=order_id,
        headers=headers
    )


@router.post("/{payment_id}/process")
def process_payment(
    payment_id: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    headers = get_headers(request)

    return GatewayService.process_payment(
        payment_id=payment_id,
        headers=headers
    )
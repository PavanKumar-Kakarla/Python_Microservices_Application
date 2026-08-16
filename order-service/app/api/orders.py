from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.dependencies.auth import validate_access_token
from app.dependencies.database import get_db
from app.repositories.order_repository import OrderRepository
from app.schemas.auth_schema import ValidateTokenResponse
from app.schemas.order import OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService
from app.clients.user_client import UserClient
from app.core.exceptions import OrderException


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


security = HTTPBearer()


@router.post("")
def create_order(
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return OrderService.create_order(
        db,
        token.email,
        credentials.credentials,
        idempotency_key
    )


@router.get(
    "",
    response_model=list[OrderResponse]
)
def get_orders(
    token: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    user = UserClient.get_user_by_email(token.email)

    if not user.is_active:
        raise OrderException(
            status_code=400,
            message="User is inactive"
        )

    return OrderRepository.get_orders_by_user_id(
        db,
        user.id
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    token: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    user = UserClient.get_user_by_email(token.email)

    if not user.is_active:
        raise OrderException(
            status_code=400,
            message="User is inactive"
        )

    order = OrderRepository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise OrderException(
            status_code=404,
            message="Order not found"
        )

    if order.user_id != user.id:
        raise OrderException(
            status_code=403,
            message="You are not authorized to access this order"
        )

    return order


@router.put(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status(
    order_id: int,
    request: OrderStatusUpdate,
    token: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return OrderService.update_order_status(
        db,
        token.email,
        order_id,
        request.status.value
    )
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import validate_access_token
from app.dependencies.database import get_db
from app.schemas.auth_schema import ValidateTokenResponse
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService
from app.core.exceptions import PaymentNotFoundException
from app.clients.user_client import UserClient


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    request: PaymentCreate,
    token: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    if not token.email:
        raise HTTPException(
            status_code=401,
            detail="User information not available"
        )

    user = UserClient.get_user_by_email(token.email)

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="User is inactive"
        )

    return PaymentService.create_payment(
        db=db,
        payment_data=request,
        user_id=user.id
    )


@router.get(
    "/order/{order_id}",
    response_model=PaymentResponse
)
def get_payment_by_order(
    order_id: int,
    token: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    if not token.email:
        raise HTTPException(
            status_code=401,
            detail="User information not available"
        )

    user = UserClient.get_user_by_email(token.email)

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="User is inactive"
        )

    payment = PaymentService.get_payment_by_order(
        db,
        order_id
    )

    if not payment:
        raise PaymentNotFoundException()

    if payment.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this payment"
        )

    return payment


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    token: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    if not token.email:
        raise HTTPException(
            status_code=401,
            detail="User information not available"
        )

    user = UserClient.get_user_by_email(token.email)

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="User is inactive"
        )

    payment = PaymentService.get_payment(
        db,
        payment_id
    )

    if not payment:
        raise PaymentNotFoundException()

    if payment.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this payment"
        )

    return payment


@router.post(
    "/{payment_id}/process",
    response_model=PaymentResponse
)
def process_payment(
    payment_id: int,
    token: ValidateTokenResponse = Depends(
        validate_access_token
    ),
    db: Session = Depends(get_db)
):
    if not token.email:
        raise HTTPException(
            status_code=401,
            detail="User information not available"
        )

    user = UserClient.get_user_by_email(
        token.email
    )

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="User is inactive"
        )

    payment = PaymentService.get_payment(
        db,
        payment_id
    )

    if not payment:
        raise PaymentNotFoundException()

    if payment.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to process this payment"
        )

    return PaymentService.process_payment(
        db,
        payment
    )
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth import validate_access_token
from app.dependencies.database import get_db
from app.schemas.auth_schema import ValidateTokenRequest
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse
)
from app.services.cart_service import CartService

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.get(
    "",
    response_model=CartResponse
)
def get_cart(
    token: ValidateTokenRequest = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return CartService.get_cart(
        db,
        token.email
    )


@router.post(
    "/items",
    status_code=status.HTTP_201_CREATED
)
def add_item(
    request: CartItemCreate,
    token: ValidateTokenRequest = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return CartService.add_item(
        db,
        token.email,
        request
    )


@router.put("/items/{product_id}")
def update_item(
    product_id: int,
    request: CartItemUpdate,
    token: ValidateTokenRequest = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return CartService.update_item(
        db,
        token.email,
        product_id,
        request
    )


@router.delete("/items/{product_id}")
def remove_item(
    product_id: int,
    token: ValidateTokenRequest = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return CartService.remove_item(
        db,
        token.email,
        product_id
    )


@router.delete("")
def clear_cart(
    token: ValidateTokenRequest = Depends(validate_access_token),
    db: Session = Depends(get_db)
):
    return CartService.clear_cart(
        db,
        token.email
    )
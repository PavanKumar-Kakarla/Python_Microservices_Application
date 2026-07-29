from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)
from app.schemas.auth_schema import ValidateTokenResponse
from app.services.product_service import ProductService
from app.dependencies.auth import validate_access_token

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    current_user: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):

    return ProductService.create_product(
        db,
        product
    )


@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_all_products(
    db: Session = Depends(get_db)
):

    return ProductService.get_all_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    return ProductService.get_product(
        db,
        product_id
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):

    return ProductService.update_product(
        db,
        product_id,
        product
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    current_user: ValidateTokenResponse = Depends(validate_access_token),
    db: Session = Depends(get_db)
):

    ProductService.delete_product(
        db,
        product_id
    )
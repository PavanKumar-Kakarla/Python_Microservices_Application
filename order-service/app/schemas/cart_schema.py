from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    created_at: datetime
    updated_at: datetime


class CartResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: list[CartItemResponse] = []
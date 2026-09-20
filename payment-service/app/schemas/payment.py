from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    order_id: int
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    payment_method: str = Field(..., min_length=1, max_length=50)


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    user_id: int
    amount: Decimal
    currency: str
    status: str
    payment_method: str
    transaction_id: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

    
from decimal import Decimal
from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: Decimal
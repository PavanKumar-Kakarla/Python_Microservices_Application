from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import OrderException


async def order_exception_handler(
    request: Request,
    exc: OrderException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message
        }
    )
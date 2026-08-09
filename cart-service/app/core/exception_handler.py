from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import CartException


async def cart_exception_handler(
    request: Request,
    exc: CartException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message
        }
    )
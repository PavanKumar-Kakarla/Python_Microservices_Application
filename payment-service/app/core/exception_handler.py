from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import PaymentServiceException
from app.core.logger import logger


async def payment_service_exception_handler(
    request: Request,
    exc: PaymentServiceException
):
    logger.warning(
        "Payment Service Exception | %s %s | %s",
        request.method,
        request.url.path,
        exc.message
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled Exception | %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        PaymentServiceException,
        payment_service_exception_handler
    )

    app.add_exception_handler(
        Exception,
        general_exception_handler
    )
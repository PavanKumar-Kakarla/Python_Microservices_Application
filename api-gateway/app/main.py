from fastapi import FastAPI

from app.core.config import settings
from app.api.gateway import router as gateway_router
from app.middleware.logger import LoggingMiddleware
from app.core.exceptions import GatewayException
from app.core.exception_handler import gateway_exception_handler


app = FastAPI(
    title=settings.APP_NAME
)


app.add_exception_handler(
    GatewayException,
    gateway_exception_handler
)

app.add_middleware(LoggingMiddleware)

app.include_router(gateway_router)


@app.get("/")
def root():

    return {
        "message": "API Gateway is running."
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


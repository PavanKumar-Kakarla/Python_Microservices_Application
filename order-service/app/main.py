from fastapi import FastAPI

from app.api.orders import router as order_router
from app.core.config import settings
from app.core.exception_handler import order_exception_handler
from app.core.exceptions import OrderException
from app.middleware.logging import LoggingMiddleware

app = FastAPI(
    title=settings.APP_NAME
)

app.add_middleware(LoggingMiddleware)

app.add_exception_handler(
    OrderException,
    order_exception_handler
)

app.include_router(order_router)


@app.get("/")
def root():
    return {
        "message": "Order Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
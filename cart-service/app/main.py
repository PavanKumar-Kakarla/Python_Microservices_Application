from fastapi import FastAPI

from app.api.carts import router as cart_router
from app.core.config import settings
from app.core.exception_handler import cart_exception_handler
from app.core.exceptions import CartException
from app.middleware.logging import LoggingMiddleware

app = FastAPI(
    title=settings.APP_NAME
)

app.add_middleware(LoggingMiddleware)

app.add_exception_handler(
    CartException,
    cart_exception_handler
)

app.include_router(cart_router)


@app.get("/")
def root():
    return {
        "message": "Cart Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
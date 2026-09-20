from fastapi import FastAPI

from app.api.payments import router as payment_router
from app.core.config import settings
from app.core.exception_handler import register_exception_handlers
from app.middleware.logging import LoggingMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.include_router(payment_router)


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
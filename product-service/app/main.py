from fastapi import FastAPI

from app.api.products import router as product_router
from app.core.config import settings
from app.core.exception_handler import register_exception_handlers
from app.middleware.logging import LoggingMiddleware

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.include_router(product_router)


@app.get("/")
def home():
    return {"message": "Product Service"}
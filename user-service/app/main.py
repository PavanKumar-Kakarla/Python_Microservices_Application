from fastapi import FastAPI

from app.api.user_profile import router as user_router
from app.core.exception_handler import register_exception_handlers
from app.middleware.logging import LoggingMiddleware

app = FastAPI(
    title="User Service",
    description="User Profile Microservice for Python E-Commerce Application",
    version="1.0.0"
)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "User service is running successfully."
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }
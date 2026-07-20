from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.core.exception_handler import register_exception_handlers

app = FastAPI(
    title="Authentication Service",
    description="Authentication Microservice for Python E-Commerce Application",
    version="1.0.0"
)

register_exception_handlers(app)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": "Authentication Service is running successfully."
    }

@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }
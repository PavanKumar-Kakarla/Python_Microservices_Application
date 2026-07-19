from fastapi import FastAPI

from app.api.auth import router as auth_router

app = FastAPI(
    title="Authentication Service",
    description="Authentication Microservice for Python E-Commerce Application",
    version="1.0.0"
)

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
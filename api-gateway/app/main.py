from fastapi import FastAPI

from app.core.config import settings
from app.api.gateway import router as gateway_router


app = FastAPI(
    title=settings.APP_NAME
)


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


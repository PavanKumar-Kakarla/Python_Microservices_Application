from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ProductAlreadyExistsException,
    ProductNotFoundException
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ProductAlreadyExistsException)
    async def product_exists_handler(
        request: Request,
        exc: ProductAlreadyExistsException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Product already exists."
            }
        )
    

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(
        request: Request,
        exc: ProductNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Product not found."
            }
        )
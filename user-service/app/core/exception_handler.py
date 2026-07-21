from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsException)
    async def user_exists_handler(
        request: Request,
        exc: UserAlreadyExistsException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": "User already exists."
            }
        )
    

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "User not found."
            }
        )
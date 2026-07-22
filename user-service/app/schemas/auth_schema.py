from pydantic import BaseModel


class ValidateTokenRequest(BaseModel):
    access_token: str


class ValidateTokenResponse(BaseModel):
    valid: bool
    email: str | None = None
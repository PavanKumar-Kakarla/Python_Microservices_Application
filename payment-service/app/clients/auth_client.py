from app.clients.base_client import BaseHttpClient
from app.core.config import settings
from app.schemas.auth_schema import ValidateTokenResponse


class AuthClient:

    @staticmethod
    def validate_token(
        access_token: str
    ) -> ValidateTokenResponse:

        response = BaseHttpClient.post(
            url=f"{settings.AUTH_SERVICE_URL}/auth/validate-token",
            json={
                "access_token": access_token
            }
        )

        return ValidateTokenResponse(
            **response.json()
        )
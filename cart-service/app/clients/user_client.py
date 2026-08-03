from app.clients.base_client import BaseHttpClient
from app.core.config import settings
from app.schemas.user_schema import UserResponse


class UserClient:

    @staticmethod
    def get_user_by_email(email: str) -> UserResponse:
        response = BaseHttpClient.get(
            f"{settings.API_GATEWAY_URL}/gateway/users/email/{email}"
        )

        return UserResponse(**response.json())
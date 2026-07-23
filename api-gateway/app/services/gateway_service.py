from app.clients.base_client import BaseHttpClient
from app.core.config import settings


class GatewayService:

    @staticmethod
    def get_user(user_id: int, headers: dict):

        response = BaseHttpClient.get(

            url=f"{settings.USER_SERVICE_URL}/users/{user_id}",

            headers=headers
        )

        return response.json()
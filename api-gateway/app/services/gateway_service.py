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


    @staticmethod
    def create_user(data: dict, headers: dict):

        response = BaseHttpClient.post(
            url=f"{settings.USER_SERVICE_URL}/users",
            headers=headers,
            data=data
        )

        return response.json()


    @staticmethod
    def update_user(user_id: int, data: dict, headers: dict):

        response = BaseHttpClient.put(
            url=f"{settings.USER_SERVICE_URL}/users/{user_id}",
            headers=headers,
            data=data
        )

        return response.json()


    @staticmethod
    def delete_user(user_id: int, headers: dict):

        response = BaseHttpClient.delete(
            url=f"{settings.USER_SERVICE_URL}/users/{user_id}",
            headers=headers
        )

        return response.status_code


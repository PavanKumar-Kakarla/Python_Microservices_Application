from app.clients.base_client import BaseHttpClient
from app.core.config import settings
from app.schemas.cart_schema import CartResponse


class CartClient:

    @staticmethod
    def get_cart(
        access_token: str
    ) -> CartResponse:

        response = BaseHttpClient.get(
            f"{settings.CART_SERVICE_URL}/cart",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        return CartResponse(**response.json())

    @staticmethod
    def clear_cart(
        access_token: str
    ):

        return BaseHttpClient.delete(
            f"{settings.CART_SERVICE_URL}/cart",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
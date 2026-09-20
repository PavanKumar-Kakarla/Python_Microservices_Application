from app.clients.base_client import BaseHttpClient
from app.core.config import settings
from app.schemas.order_schema import OrderResponse
import httpx


class OrderClient:

    @staticmethod
    def get_order(
        order_id: int,
        access_token: str
    ) -> OrderResponse | None:

        try:
            response = BaseHttpClient.get(
                url=f"{settings.ORDER_SERVICE_URL}/orders/{order_id}",
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )

            return OrderResponse(**response.json())

        except httpx.HTTPStatusError as exc:

            if exc.response.status_code == 404:
                return None

            raise


    @staticmethod
    def confirm_order(
        order_id: int,
        access_token: str
    ) -> OrderResponse:

        response = BaseHttpClient.put(
                    url=f"{settings.ORDER_SERVICE_URL}/orders/{order_id}/status",
                    json={
                        "status": "CONFIRMED"
                    },
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    }
                )
        
        return OrderResponse(**response.json())
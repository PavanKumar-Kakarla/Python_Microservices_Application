from app.clients.base_client import BaseHttpClient
from app.core.config import settings
from app.schemas.product_schema import ProductResponse


class ProductClient:

    @staticmethod
    def get_product(product_id: int) -> ProductResponse:

        response = BaseHttpClient.get(
            f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}"
        )

        return ProductResponse(**response.json())
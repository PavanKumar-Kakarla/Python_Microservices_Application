from app.clients.base_client import BaseHttpClient
from app.core.config import settings
from app.schemas.product_schema import ProductResponse


class ProductClient:

    BASE_URL = settings.PRODUCT_SERVICE_URL

    @classmethod
    def get_product(
        cls,
        product_id: int
    ) -> ProductResponse:

        response = BaseHttpClient.get(
            f"{cls.BASE_URL}/products/{product_id}"
        )

        return ProductResponse(
            **response.json()
        )
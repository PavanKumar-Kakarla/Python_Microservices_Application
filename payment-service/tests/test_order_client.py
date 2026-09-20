import httpx
from unittest.mock import MagicMock, patch

from app.clients.order_client import OrderClient


def test_get_order_returns_none_for_404():

    response = MagicMock()
    response.status_code = 404

    error = httpx.HTTPStatusError(
        "Order not found",
        request=MagicMock(),
        response=response,
    )

    with patch(
        "app.clients.order_client.BaseHttpClient.get",
        side_effect=error,
    ):

        result = OrderClient.get_order(
            order_id=999,
            access_token="test-access-token",
        )

    assert result is None


from decimal import Decimal


def test_get_order_returns_order():

    response = MagicMock()

    response.json.return_value = {
        "id": 100,
        "user_id": 1,
        "status": "PENDING",
        "total_amount": "500.00",
    }

    with patch(
        "app.clients.order_client.BaseHttpClient.get",
        return_value=response,
    ):

        result = OrderClient.get_order(
            order_id=100,
            access_token="test-access-token",
        )

    assert result.id == 100
    assert result.user_id == 1
    assert result.status == "PENDING"
    assert result.total_amount == Decimal("500.00")
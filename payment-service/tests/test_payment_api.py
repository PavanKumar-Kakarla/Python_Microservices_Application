from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.dependencies.auth import validate_access_token
from app.dependencies.database import get_db
from app.schemas.auth_schema import ValidateTokenResponse
from app.schemas.user_schema import UserResponse


client = TestClient(app)


def override_auth():
    return ValidateTokenResponse(
        valid=True,
        email="test@test.com",
        user_id=None,
    )


def override_db():
    db = MagicMock()
    yield db


app.dependency_overrides[validate_access_token] = override_auth
app.dependency_overrides[get_db] = override_db


def create_user():
    now = datetime.now(timezone.utc)

    return UserResponse(
        id=3,
        email="test@test.com",
        first_name="Test",
        last_name="User",
        phone="9999999999",
        is_active=True,
        created_at=now,
        updated_at=now,
    )


def create_payment():
    payment = MagicMock()

    payment.id = 1
    payment.order_id = 4
    payment.user_id = 3
    payment.amount = Decimal("196000.00")
    payment.currency = "INR"
    payment.status = "PENDING"
    payment.payment_method = "CARD"
    payment.transaction_id = None

    return payment


def test_create_payment():
    payment = create_payment()

    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=create_user(),
    ), patch(
        "app.api.payments.PaymentService.create_payment",
        return_value=payment,
    ):

        response = client.post(
            "/payments",
            json={
                "order_id": 4,
                "amount": 196000,
                "currency": "INR",
                "payment_method": "CARD",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["order_id"] == 4
    assert data["user_id"] == 3
    assert data["amount"] == "196000.00"
    assert data["currency"] == "INR"
    assert data["status"] == "PENDING"
    assert data["payment_method"] == "CARD"
    assert data["transaction_id"] is None


def test_get_payment():
    payment = create_payment()

    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=create_user(),
    ), patch(
        "app.api.payments.PaymentService.get_payment",
        return_value=payment,
    ):

        response = client.get("/payments/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["user_id"] == 3
    assert data["status"] == "PENDING"


def test_get_payment_by_order():
    payment = create_payment()

    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=create_user(),
    ), patch(
        "app.api.payments.PaymentService.get_payment_by_order",
        return_value=payment,
    ):

        response = client.get("/payments/order/4")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["order_id"] == 4


def test_get_payment_not_found():
    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=create_user(),
    ), patch(
        "app.api.payments.PaymentService.get_payment",
        return_value=None,
    ):

        response = client.get("/payments/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


def test_get_payment_forbidden():
    payment = create_payment()

    other_user = create_user()
    other_user.id = 5

    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=other_user,
    ), patch(
        "app.api.payments.PaymentService.get_payment",
        return_value=payment,
    ):

        response = client.get("/payments/1")

    assert response.status_code == 403

    assert response.json()["detail"] == (
        "You are not authorized to access this payment"
    )


def test_process_payment():
    payment = create_payment()

    processed_payment = create_payment()
    processed_payment.status = "SUCCESS"
    processed_payment.transaction_id = "TXN-TEST-001"

    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=create_user(),
    ), patch(
        "app.api.payments.PaymentService.get_payment",
        return_value=payment,
    ), patch(
        "app.api.payments.PaymentService.process_payment",
        return_value=processed_payment,
    ):

        response = client.post(
            "/payments/1/process"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["transaction_id"] == "TXN-TEST-001"


def test_process_payment_forbidden():
    payment = create_payment()

    other_user = create_user()
    other_user.id = 5

    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=other_user,
    ), patch(
        "app.api.payments.PaymentService.get_payment",
        return_value=payment,
    ):

        response = client.post(
            "/payments/1/process"
        )

    assert response.status_code == 403

    assert response.json()["detail"] == (
        "You are not authorized to process this payment"
    )


def test_process_payment_not_found():
    with patch(
        "app.api.payments.UserClient.get_user_by_email",
        return_value=create_user(),
    ), patch(
        "app.api.payments.PaymentService.get_payment",
        return_value=None,
    ):

        response = client.post(
            "/payments/999/process"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from app.models import Payment
from app.schemas import PaymentCreate
from app.services.payment_service import PaymentService
from app.schemas.order_schema import OrderResponse
from app.core.exceptions import PaymentProcessingException
from sqlalchemy.exc import IntegrityError


def create_test_order(
    order_id=100,
    user_id=1,
    status="PENDING",
    total_amount=500.00,
):
    return OrderResponse(
        id=order_id,
        user_id=user_id,
        status=status,
        total_amount=Decimal(str(total_amount)),
    )


def create_test_payment(
    payment_id=1,
    order_id=100,
    user_id=1,
    amount=500.00,
    status="PENDING",
    transaction_id=None,
):
    return Payment(
        id=payment_id,
        order_id=order_id,
        user_id=user_id,
        amount=amount,
        currency="INR",
        status=status,
        payment_method="CARD",
        transaction_id=transaction_id,
    )


def test_create_payment():
    db = MagicMock()

    payment_data = PaymentCreate(
        order_id=100,
        amount=500,
        currency="INR",
        payment_method="CARD",
    )

    expected_payment = create_test_payment()

    order = create_test_order(
        order_id=100,
        user_id=1,
        status="PENDING",
        total_amount=500.00,
    )

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=None,
    ), patch(
        "app.services.payment_service.OrderClient.get_order",
        return_value=order,
    ), patch(
        "app.services.payment_service.PaymentRepository.create",
        return_value=expected_payment,
    ):

        result = PaymentService.create_payment(
            db=db,
            payment_data=payment_data,
            user_id=1,
            access_token="test-access-token",
        )

    assert result is expected_payment
    assert result.order_id == 100
    assert result.user_id == 1
    assert result.status == "PENDING"


def test_create_payment_returns_existing_payment():
    db = MagicMock()

    payment_data = PaymentCreate(
        order_id=100,
        amount=500,
        currency="INR",
        payment_method="CARD",
    )

    existing_payment = create_test_payment()

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=existing_payment,
    ), patch(
        "app.services.payment_service.PaymentRepository.create"
    ) as mock_create:

        result = PaymentService.create_payment(
            db=db,
            payment_data=payment_data,
            user_id=1,
            access_token="test-access-token",
        )

    assert result is existing_payment
    mock_create.assert_not_called()


def test_get_payment():
    db = MagicMock()

    expected_payment = create_test_payment()

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_id",
        return_value=expected_payment,
    ):

        result = PaymentService.get_payment(
            db,
            1,
        )

    assert result is expected_payment


def test_get_payment_returns_none():
    db = MagicMock()

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_id",
        return_value=None,
    ):

        result = PaymentService.get_payment(
            db,
            999,
        )

    assert result is None


def test_get_payment_by_order():
    db = MagicMock()

    expected_payment = create_test_payment(
        order_id=200
    )

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=expected_payment,
    ):

        result = PaymentService.get_payment_by_order(
            db,
            200,
        )

    assert result is expected_payment
    assert result.order_id == 200


def test_process_payment():
    db = MagicMock()

    payment = create_test_payment(
        status="PENDING"
    )

    with patch(
        "app.services.payment_service.PaymentRepository.update",
        return_value=payment,
    ), patch(
        "app.services.payment_service.OrderClient.confirm_order"
    ) as mock_confirm_order:

        result = PaymentService.process_payment(
            db=db,
            payment=payment,
            access_token="test-access-token",
        )

    assert result.status == "SUCCESS"
    assert result.transaction_id is not None
    assert result.transaction_id.startswith("TXN-")

    mock_confirm_order.assert_called_once_with(
        order_id=payment.order_id,
        access_token="test-access-token",
    )


def test_process_payment_already_successful():
    db = MagicMock()

    payment = create_test_payment(
        status="SUCCESS",
        transaction_id="TXN-EXISTING-001",
    )

    with patch(
        "app.services.payment_service.PaymentRepository.update"
    ) as mock_update, patch(
        "app.services.payment_service.OrderClient.confirm_order"
    ) as mock_confirm_order:

        result = PaymentService.process_payment(
            db=db,
            payment=payment,
            access_token="test-access-token",
        )

    assert result.status == "SUCCESS"
    assert result.transaction_id == "TXN-EXISTING-001"

    mock_update.assert_not_called()
    mock_confirm_order.assert_not_called()


def test_create_payment_order_belongs_to_different_user():
    db = MagicMock()

    payment_data = PaymentCreate(
        order_id=100,
        amount=500,
        currency="INR",
        payment_method="CARD",
    )

    order = create_test_order(
        order_id=100,
        user_id=2,
        status="PENDING",
        total_amount=500.00,
    )

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=None,
    ), patch(
        "app.services.payment_service.OrderClient.get_order",
        return_value=order,
    ):

        with pytest.raises(PaymentProcessingException) as exc:
            PaymentService.create_payment(
                db=db,
                payment_data=payment_data,
                user_id=1,
                access_token="test-access-token",
            )

    assert exc.value.message == (
        "You are not authorized to create payment for this order"
    )


def test_create_payment_order_not_pending():
    db = MagicMock()

    payment_data = PaymentCreate(
        order_id=100,
        amount=500,
        currency="INR",
        payment_method="CARD",
    )

    order = create_test_order(
        order_id=100,
        user_id=1,
        status="CONFIRMED",
        total_amount=500.00,
    )

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=None,
    ), patch(
        "app.services.payment_service.OrderClient.get_order",
        return_value=order,
    ):

        with pytest.raises(PaymentProcessingException) as exc:
            PaymentService.create_payment(
                db=db,
                payment_data=payment_data,
                user_id=1,
                access_token="test-access-token",
            )

    assert exc.value.message == (
        "Payment cannot be created for order status is CONFIRMED"
    )


def test_create_payment_amount_mismatch():
    db = MagicMock()

    payment_data = PaymentCreate(
        order_id=100,
        amount=400,
        currency="INR",
        payment_method="CARD",
    )

    order = create_test_order(
        order_id=100,
        user_id=1,
        status="PENDING",
        total_amount=500.00,
    )

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=None,
    ), patch(
        "app.services.payment_service.OrderClient.get_order",
        return_value=order,
    ):

        with pytest.raises(PaymentProcessingException) as exc:
            PaymentService.create_payment(
                db=db,
                payment_data=payment_data,
                user_id=1,
                access_token="test-access-token",
            )

    assert exc.value.message == (
        "Payment amount does not match order total amount"
    )


def test_process_payment_invalid_status():
    db = MagicMock()

    payment = create_test_payment(
        status="FAILED"
    )

    with patch(
        "app.services.payment_service.OrderClient.confirm_order"
    ) as mock_confirm_order:

        with pytest.raises(PaymentProcessingException) as exc:
            PaymentService.process_payment(
                db=db,
                payment=payment,
                access_token="test-access-token",
            )

    assert exc.value.message == (
        "Payment cannot be processed from status: FAILED"
    )

    mock_confirm_order.assert_not_called()


def test_create_payment_order_not_found():
    db = MagicMock()

    payment_data = PaymentCreate(
        order_id=999,
        amount=500,
        currency="INR",
        payment_method="CARD",
    )

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=None,
    ), patch(
        "app.services.payment_service.OrderClient.get_order",
        return_value=None,
    ):

        with pytest.raises(PaymentProcessingException) as exc:
            PaymentService.create_payment(
                db=db,
                payment_data=payment_data,
                user_id=1,
                access_token="test-access-token",
            )

    assert exc.value.message == "Order not found"


def test_create_payment_handles_duplicate_order_id():
    db = MagicMock()

    payment_data = PaymentCreate(
        order_id=100,
        amount=500,
        currency="INR",
        payment_method="CARD",
    )

    order = create_test_order(
        order_id=100,
        user_id=1,
        status="PENDING",
        total_amount=500.00,
    )

    existing_payment = create_test_payment(
        payment_id=10,
        order_id=100,
        user_id=1,
        amount=500.00,
        status="PENDING",
    )

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        side_effect=[None, existing_payment],
    ), patch(
        "app.services.payment_service.OrderClient.get_order",
        return_value=order,
    ), patch(
        "app.services.payment_service.PaymentRepository.create",
        side_effect=IntegrityError(
            "duplicate",
            params=None,
            orig=Exception("duplicate order_id"),
        ),
    ):
        result = PaymentService.create_payment(
            db=db,
            payment_data=payment_data,
            user_id=1,
            access_token="test-access-token",
        )

    db.rollback.assert_called_once()

    assert result is existing_payment
    assert result.order_id == 100
    assert result.user_id == 1
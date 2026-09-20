from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from app.models import Payment
from app.schemas import PaymentCreate
from app.services.payment_service import PaymentService


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

    with patch(
        "app.services.payment_service.PaymentRepository.get_by_order_id",
        return_value=None,
    ), patch(
        "app.services.payment_service.PaymentRepository.create",
        return_value=expected_payment,
    ):

        result = PaymentService.create_payment(
            db=db,
            payment_data=payment_data,
            user_id=1,
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
    ):

        result = PaymentService.process_payment(
            db,
            payment,
        )

    assert result.status == "SUCCESS"
    assert result.transaction_id is not None
    assert result.transaction_id.startswith("TXN-")


def test_process_payment_already_successful():
    db = MagicMock()

    payment = create_test_payment(
        status="SUCCESS",
        transaction_id="TXN-EXISTING-001",
    )

    with patch(
        "app.services.payment_service.PaymentRepository.update"
    ) as mock_update:

        result = PaymentService.process_payment(
            db,
            payment,
        )

    assert result.status == "SUCCESS"
    assert result.transaction_id == "TXN-EXISTING-001"

    mock_update.assert_not_called()
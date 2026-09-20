import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models import Payment
from app.repositories import PaymentRepository


TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def create_test_payment(
    order_id=100,
    user_id=1,
    amount=500.00,
    status="PENDING",
    transaction_id=None,
):
    return Payment(
        order_id=order_id,
        user_id=user_id,
        amount=amount,
        currency="INR",
        status=status,
        payment_method="CARD",
        transaction_id=transaction_id,
    )


def test_create_payment(db):
    payment = create_test_payment()

    result = PaymentRepository.create(
        db,
        payment
    )

    assert result.id is not None
    assert result.order_id == 100
    assert result.user_id == 1
    assert result.amount == 500.00
    assert result.status == "PENDING"


def test_get_by_id(db):
    payment = create_test_payment()

    created_payment = PaymentRepository.create(
        db,
        payment
    )

    result = PaymentRepository.get_by_id(
        db,
        created_payment.id
    )

    assert result is not None
    assert result.id == created_payment.id
    assert result.order_id == 100


def test_get_by_order_id(db):
    payment = create_test_payment(
        order_id=200
    )

    PaymentRepository.create(
        db,
        payment
    )

    result = PaymentRepository.get_by_order_id(
        db,
        200
    )

    assert result is not None
    assert result.order_id == 200


def test_get_by_transaction_id(db):
    payment = create_test_payment(
        transaction_id="TXN-TEST-001"
    )

    PaymentRepository.create(
        db,
        payment
    )

    result = PaymentRepository.get_by_transaction_id(
        db,
        "TXN-TEST-001"
    )

    assert result is not None
    assert result.transaction_id == "TXN-TEST-001"


def test_get_by_id_returns_none_for_missing_payment(db):
    result = PaymentRepository.get_by_id(
        db,
        9999
    )

    assert result is None


def test_get_by_order_id_returns_none_for_missing_payment(db):
    result = PaymentRepository.get_by_order_id(
        db,
        9999
    )

    assert result is None


def test_update_payment(db):
    payment = create_test_payment()

    created_payment = PaymentRepository.create(
        db,
        payment
    )

    created_payment.status = "SUCCESS"
    created_payment.transaction_id = "TXN-UPDATE-001"

    result = PaymentRepository.update(
        db,
        created_payment
    )

    assert result.status == "SUCCESS"
    assert result.transaction_id == "TXN-UPDATE-001"
import threading
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models import Payment


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_payment(order_id: int):
    db = TestSessionLocal()

    try:
        payment = Payment(
            order_id=order_id,
            user_id=1,
            amount=500,
            currency="INR",
            status="PENDING",
            payment_method="CARD",
            transaction_id=None,
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return {
            "success": True,
            "payment_id": payment.id,
        }

    except Exception as exc:
        db.rollback()

        return {
            "success": False,
            "error": type(exc).__name__,
        }

    finally:
        db.close()


def test_concurrent_payment_creation():
    order_id = 99999

    # Make sure the test starts clean.
    cleanup_db = TestSessionLocal()

    try:
        existing = (
            cleanup_db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )

        if existing:
            cleanup_db.delete(existing)
            cleanup_db.commit()

    finally:
        cleanup_db.close()

    barrier = threading.Barrier(2)

    def worker():
        barrier.wait()
        return create_payment(order_id)

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(
            executor.map(
                lambda _: worker(),
                range(2),
            )
        )

    success_count = sum(
        result["success"]
        for result in results
    )

    assert success_count == 1

    verify_db = TestSessionLocal()

    try:
        payments = (
            verify_db.query(Payment)
            .filter(Payment.order_id == order_id)
            .all()
        )

        assert len(payments) == 1

    finally:
        verify_db.close()
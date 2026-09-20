from sqlalchemy.orm import Session

from app.models import Payment


class PaymentRepository:

    @staticmethod
    def create(db: Session, payment: Payment) -> Payment:
        db.add(payment)
        db.flush()
        db.refresh(payment)

        return payment

    @staticmethod
    def get_by_id(db: Session, payment_id: int) -> Payment | None:
        return (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

    @staticmethod
    def get_by_order_id(db: Session, order_id: int) -> Payment | None:
        return (
            db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )

    @staticmethod
    def get_by_transaction_id(
        db: Session,
        transaction_id: str
    ) -> Payment | None:
        return (
            db.query(Payment)
            .filter(Payment.transaction_id == transaction_id)
            .first()
        )

    @staticmethod
    def update(db: Session, payment: Payment) -> Payment:
        db.commit()
        db.refresh(payment)

        return payment
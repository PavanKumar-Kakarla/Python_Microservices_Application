from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import Payment
from app.repositories import PaymentRepository
from app.schemas import PaymentCreate
from app.core.exceptions import PaymentProcessingException


class PaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        payment_data: PaymentCreate,
        user_id: int
    ) -> Payment:

        # Check whether a payment already exists for this order
        existing_payment = PaymentRepository.get_by_order_id(
            db,
            payment_data.order_id
        )

        if existing_payment:
            return existing_payment

        payment = Payment(
            order_id=payment_data.order_id,
            user_id=user_id,
            amount=Decimal(payment_data.amount),
            currency=payment_data.currency.upper(),
            status="PENDING",
            payment_method=payment_data.payment_method,
            transaction_id=None,
        )

        return PaymentRepository.create(db, payment)

    @staticmethod
    def get_payment(
        db: Session,
        payment_id: int
    ) -> Payment | None:

        return PaymentRepository.get_by_id(
            db,
            payment_id
        )

    @staticmethod
    def get_payment_by_order(
        db: Session,
        order_id: int
    ) -> Payment | None:

        return PaymentRepository.get_by_order_id(
            db,
            order_id
        )

    @staticmethod
    def process_payment(
        db: Session,
        payment: Payment
    ) -> Payment:

        if payment.status == "SUCCESS":
            return payment

        if payment.status != "PENDING":
            raise PaymentProcessingException(
                message=f"Payment cannot be processed from status: {payment.status}"
            )

        payment.status = "SUCCESS"
        payment.transaction_id = (
            f"TXN-{uuid4().hex[:20].upper()}"
        )

        return PaymentRepository.update(
            db,
            payment
        )
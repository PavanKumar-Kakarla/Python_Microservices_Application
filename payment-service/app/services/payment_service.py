from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import Payment
from app.repositories import PaymentRepository
from app.schemas import PaymentCreate
from app.core.exceptions import PaymentProcessingException
from app.clients.order_client import OrderClient


class PaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        payment_data: PaymentCreate,
        user_id: int,
        access_token: str
    ) -> Payment:

        # Check whether a payment already exists for this order
        existing_payment = PaymentRepository.get_by_order_id(
            db,
            payment_data.order_id
        )

        if existing_payment:
            return existing_payment

        # Get Order from Order Service
        order = OrderClient.get_order(
            order_id=payment_data.order_id,
            access_token=access_token
        )

        # Verify order exists
        if not order:
            raise PaymentProcessingException(
                message="Order not found"
            )

        # Verify order ownership
        if order.user_id != user_id:
            raise PaymentProcessingException(
                message="You are not authorized to create payment for this order"
            )

        # Verify order status
        if order.status != "PENDING":
            raise PaymentProcessingException(
                message=f"Payment cannot be created for order status is {order.status}"
            )

        # Verify payment amount
        if Decimal(payment_data.amount) != order.total_amount:
            raise PaymentProcessingException(
                message="Payment amount does not match order total amount"
            )
        
        # Create Payment
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
        payment: Payment,
        access_token: str
    ) -> Payment:

        # Already successful - idempotent behavior
        if payment.status == "SUCCESS":
            return payment

        # Only PENDING payments can be processed
        if payment.status != "PENDING":
            raise PaymentProcessingException(
                message=f"Payment cannot be processed from status: {payment.status}"
            )

        # Process Payment
        payment.status = "SUCCESS"
        payment.transaction_id = (
            f"TXN-{uuid4().hex[:20].upper()}"
        )

        payment = PaymentRepository.update(
            db,
            payment
        )

        # Confirm the order after successful payment
        OrderClient.confirm_order(
            order_id=payment.order_id,
            access_token=access_token
        )

        return payment
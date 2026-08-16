from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.clients.cart_client import CartClient
from app.clients.product_client import ProductClient
from app.clients.user_client import UserClient
from app.core.exceptions import OrderException
from app.repositories.order_repository import OrderRepository


class OrderService:

    @staticmethod
    def create_order(
        db: Session,
        email: str,
        access_token: str,
        idempotency_key: str
    ):

        # 1. Get user
        user = UserClient.get_user_by_email(email)

        if not user.is_active:
            raise OrderException(
                status_code=400,
                message="User is inactive"
            )

        # 2. Get user's cart
        cart = CartClient.get_cart(
            access_token
        )

        # 3. Check cart
        if not cart.items:
            raise OrderException(
                status_code=400,
                message="Cannot create order from an empty cart"
            )

        order_items = []
        total_amount = Decimal("0.00")

        # 4. Validate products and calculate total
        for cart_item in cart.items:

            product = ProductClient.get_product(
                cart_item.product_id
            )

            if not product.is_active:
                raise OrderException(
                    status_code=400,
                    message=f"Product {product.id} is inactive"
                )

            unit_price = product.price

            subtotal = (
                unit_price *
                cart_item.quantity
            )

            total_amount += subtotal

            order_items.append(
                {
                    "product_id": product.id,
                    "quantity": cart_item.quantity,
                    "unit_price": unit_price
                }
            )

        # 5. Checking the existing order with idempotency key
        existing_record = OrderRepository.get_idempotency_record(
            db=db,
            user_id=user.id,
            idempotency_key=idempotency_key
        )

        if existing_record:
            existing_order = OrderRepository.get_order_by_id(
                db=db,
                order_id=existing_record.order_id
            )

            if existing_order:
                return existing_order
        

        try:

            # 6. Create order and order items
            order = OrderRepository.create_order_with_items(
                db=db,
                user_id=user.id,
                status="PENDING",
                total_amount=total_amount,
                items=order_items
            )

            # 7. Create idempotency record
            OrderRepository.create_idempotency_record(
                db=db,
                user_id=user.id,
                idempotency_key=idempotency_key,
                order_id=order.id
            )

            # Commit everything together
            db.commit()

            db.refresh(order)

        except IntegrityError:

            # Another concurrent request may have
            # inserted the same idempotency key
            db.rollback()

            existing_record = OrderRepository.get_idempotency_record(
                db=db,
                user_id=user.id,
                idempotency_key=idempotency_key
            )

            if existing_record:

                existing_order = OrderRepository.get_order_by_id(
                    db=db,
                    order_id=existing_record.order_id
                )

                if existing_order:
                    return existing_order

            raise

        # 8. Clear cart
        try:
            CartClient.clear_cart(
                access_token
            )

        except Exception as exc:
            raise OrderException(
                status_code=503,
                message=(
                    "Order was created successfully, "
                    "but cart could not be cleared"
                )
            ) from exc

        return order


    @staticmethod
    def update_order_status(
        db: Session,
        email: str,
        order_id: int,
        new_status: str
    ):

        user = UserClient.get_user_by_email(email)

        if not user.is_active:
            raise OrderException(
                status_code=400,
                message="User is inactive"
            )

        order = OrderRepository.get_order_by_id(
            db,
            order_id
        )

        if not order:
            raise OrderException(
                status_code=404,
                message="Order not found"
            )

        if order.user_id != user.id:
            raise OrderException(
                status_code=403,
                message="You are not authorized to update this order"
            )

        allowed_transitions = {
            "PENDING": ["CONFIRMED", "CANCELLED"],
            "CONFIRMED": ["SHIPPED"],
            "SHIPPED": ["DELIVERED"],
            "DELIVERED": [],
            "CANCELLED": []
        }

        current_status = order.status

        if new_status not in allowed_transitions.get(
            current_status,
            []
        ):
            raise OrderException(
                status_code=400,
                message=(
                    f"Invalid order status transition: "
                    f"{current_status} -> {new_status}"
                )
            )

        return OrderRepository.update_order_status(
            db,
            order,
            new_status
        )
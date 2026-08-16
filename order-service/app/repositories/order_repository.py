from sqlalchemy.orm import Session, joinedload

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order_idempotency import OrderIdempotency


class OrderRepository:

    @staticmethod
    def create_order(
        db: Session,
        user_id: int,
        status: str,
        total_amount
    ) -> Order:

        order = Order(
            user_id=user_id,
            status=status,
            total_amount=total_amount
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def create_order_item(
        db: Session,
        order_id: int,
        product_id: int,
        quantity: int,
        unit_price
    ) -> OrderItem:

        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        db.add(order_item)
        db.commit()
        db.refresh(order_item)

        return order_item

    @staticmethod
    def get_order_by_id(
        db: Session,
        order_id: int
    ) -> Order | None:

        return (
            db.query(Order)
            .options(
                joinedload(Order.items)
            )
            .filter(Order.id == order_id)
            .first()
        )

    @staticmethod
    def get_orders_by_user_id(
        db: Session,
        user_id: int
    ) -> list[Order]:

        return (
            db.query(Order)
            .options(
                joinedload(Order.items)
            )
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    @staticmethod
    def delete_order(
        db: Session,
        order: Order
    ) -> None:

        db.delete(order)
        db.commit()


    @staticmethod
    def create_order_with_items(
        db: Session,
        user_id: int,
        status: str,
        total_amount,
        items: list[dict]
    ) -> Order:

        order = Order(
            user_id=user_id,
            status=status,
            total_amount=total_amount
        )

        db.add(order)
        db.flush()

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"]
            )

            db.add(order_item)

        db.flush()

        return order
    

    @staticmethod
    def update_order_status(
        db: Session,
        order: Order,
        status: str
    ) -> Order:

        order.status = status

        db.commit()
        db.refresh(order)

        return order


    @staticmethod
    def get_idempotency_record(
        db: Session,
        user_id: int,
        idempotency_key: str
    ) -> OrderIdempotency | None:

        return (
            db.query(OrderIdempotency)
            .filter(
                OrderIdempotency.user_id == user_id,
                OrderIdempotency.idempotency_key == idempotency_key
            )
            .first()
        )


    @staticmethod
    def create_idempotency_record(
        db: Session,
        user_id: int,
        idempotency_key: str,
        order_id: int
    ) -> OrderIdempotency:

        record = OrderIdempotency(
            user_id=user_id,
            idempotency_key=idempotency_key,
            order_id=order_id
        )

        db.add(record)
        db.flush()

        return record
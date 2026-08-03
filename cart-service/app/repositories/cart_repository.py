from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem


class CartRepository:

    @staticmethod
    def get_cart_by_user_id(
        db: Session,
        user_id: int
    ) -> Cart | None:
        return (
            db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )

    @staticmethod
    def create_cart(
        db: Session,
        user_id: int
    ) -> Cart:
        cart = Cart(
            user_id=user_id
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)

        return cart

    @staticmethod
    def get_cart_item(
        db: Session,
        cart_id: int,
        product_id: int
    ) -> CartItem | None:
        return (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id
            )
            .first()
        )

    @staticmethod
    def add_cart_item(
        db: Session,
        cart_id: int,
        product_id: int,
        quantity: int,
        unit_price: Decimal
    ) -> CartItem:
        item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        db.add(item)
        db.commit()
        db.refresh(item)

        return item

    @staticmethod
    def update_cart_item_quantity(
        db: Session,
        item: CartItem,
        quantity: int
    ) -> CartItem:
        item.quantity = quantity

        db.commit()
        db.refresh(item)

        return item

    @staticmethod
    def delete_cart_item(
        db: Session,
        item: CartItem
    ) -> None:
        db.delete(item)
        db.commit()

    @staticmethod
    def clear_cart(
        db: Session,
        cart: Cart
    ) -> None:
        for item in cart.items:
            db.delete(item)

        db.commit()
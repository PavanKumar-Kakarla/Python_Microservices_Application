from sqlalchemy.orm import Session

from app.clients.product_client import ProductClient
from app.core.exceptions import CartException
from app.models.cart import Cart
from app.repositories.cart_repository import CartRepository
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
)
from app.clients.user_client import UserClient


class CartService:

    @staticmethod
    def get_cart(
        db: Session,
        email: str
    ) -> Cart:

        user = CartService.get_user(email)

        cart = CartRepository.get_cart_by_user_id(
            db,
            user.id
        )

        if not cart:
            cart = CartRepository.create_cart(
                db,
                user.id
            )

        return cart


    @staticmethod
    def add_item(
        db: Session,
        email: str,
        request: CartItemCreate
    ):

        cart = CartService.get_cart(
            db,
            email
        )

        product = ProductClient.get_product(
            request.product_id
        )

        if not product.is_active:
            raise CartException(
                status_code=400,
                message="Product is inactive"
            )

        existing_item = CartRepository.get_cart_item(
            db,
            cart.id,
            request.product_id
        )

        if existing_item:

            return CartRepository.update_cart_item_quantity(
                db,
                existing_item,
                existing_item.quantity + request.quantity
            )

        return CartRepository.add_cart_item(
            db,
            cart.id,
            request.product_id,
            request.quantity,
            product.price
        )


    @staticmethod
    def update_item(
        db: Session,
        email: str,
        product_id: int,
        request: CartItemUpdate
    ):

        cart = CartService.get_cart(
            db,
            email
        )

        item = CartRepository.get_cart_item(
            db,
            cart.id,
            product_id
        )

        if not item:
            raise CartException(
                status_code=404,
                message="Product not found in cart"
            )

        return CartRepository.update_cart_item_quantity(
            db,
            item,
            request.quantity
        )


    @staticmethod
    def remove_item(
        db: Session,
        email: str,
        product_id: int
    ):

        cart = CartService.get_cart(
            db,
            email
        )

        item = CartRepository.get_cart_item(
            db,
            cart.id,
            product_id
        )

        if not item:
            raise CartException(
                status_code=404,
                message="Product not found in cart"
            )

        CartRepository.delete_cart_item(
            db,
            item
        )

        return {
            "message": "Product removed from cart"
        }


    @staticmethod
    def clear_cart(
        db: Session,
        email: str,
    ):

        cart = CartService.get_cart(
            db,
            email
        )

        CartRepository.clear_cart(
            db,
            cart
        )

        return {
            "message": "Cart cleared successfully"
        }


    @staticmethod
    def get_user(email: str):
        return UserClient.get_user_by_email(email)
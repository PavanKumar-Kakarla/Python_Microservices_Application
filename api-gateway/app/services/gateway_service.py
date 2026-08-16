from app.clients.base_client import BaseHttpClient
from app.core.config import settings


class GatewayService:

    # ==============================
    # User Service
    # ==============================

    @staticmethod
    def get_user(user_id: int, headers: dict):

        response = BaseHttpClient.get(

            url=f"{settings.USER_SERVICE_URL}/users/{user_id}",

            headers=headers
        )

        return response.json()


    @staticmethod
    def create_user(data: dict, headers: dict):

        response = BaseHttpClient.post(
            url=f"{settings.USER_SERVICE_URL}/users",
            headers=headers,
            data=data
        )

        return response.json()


    @staticmethod
    def update_user(user_id: int, data: dict, headers: dict):

        response = BaseHttpClient.put(
            url=f"{settings.USER_SERVICE_URL}/users/{user_id}",
            headers=headers,
            data=data
        )

        return response.json()


    @staticmethod
    def delete_user(user_id: int, headers: dict):

        response = BaseHttpClient.delete(
            url=f"{settings.USER_SERVICE_URL}/users/{user_id}",
            headers=headers
        )

        return response.status_code



    # ==============================
    # Product Service
    # ==============================

    @staticmethod
    def get_products(headers: dict):

        response = BaseHttpClient.get(
            url=f"{settings.PRODUCT_SERVICE_URL}/products",
            headers=headers
        )

        return response.json()


    @staticmethod
    def get_product(product_id: int, headers: dict):

        response = BaseHttpClient.get(
            url=f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}",
            headers=headers
        )

        return response.json()


    @staticmethod
    def create_product(data: dict, headers: dict):

        response = BaseHttpClient.post(
            url=f"{settings.PRODUCT_SERVICE_URL}/products",
            headers=headers,
            data=data
        )

        return response.json()


    @staticmethod
    def update_product(product_id: int, data: dict, headers: dict):

        response = BaseHttpClient.put(
            url=f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}",
            headers=headers,
            data=data
        )

        return response.json()


    @staticmethod
    def delete_product(product_id: int, headers: dict):

        response = BaseHttpClient.delete(
            url=f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}",
            headers=headers
        )

        return response.status_code


    @staticmethod
    def get_user_by_email(email: str):
        response = BaseHttpClient.get(
            url=f"{settings.USER_SERVICE_URL}/users/email/{email}"
        )

        return response.json()


    @staticmethod
    def get_cart(headers: dict):

        response = BaseHttpClient.get(
            url=f"{settings.CART_SERVICE_URL}/cart",
            headers=headers
        )

        return response.json()


    @staticmethod
    def add_item(data: dict, headers: dict):

        response = BaseHttpClient.post(
            url=f"{settings.CART_SERVICE_URL}/cart/items",
            headers=headers,
            data=data
        )

        return response.json()


    @staticmethod
    def update_item(headers: dict, product_id: int, data: dict):

        response = BaseHttpClient.put(
            url=f"{settings.CART_SERVICE_URL}/cart/items/{product_id}",
            headers=headers,
            data=data
        )

        return response.json()
    

    @staticmethod
    def remove_item(headers: dict, product_id: int):

        response = BaseHttpClient.delete(
            url=f"{settings.CART_SERVICE_URL}/cart/items/{product_id}",
            headers=headers
        )

        return response.status_code


    @staticmethod
    def clear_cart(headers: dict):

        response = BaseHttpClient.delete(
            url=f"{settings.CART_SERVICE_URL}/cart",
            headers=headers
        )

        return response.status_code


    @staticmethod
    def get_orders(headers: dict):

        response = BaseHttpClient.get(
            url=f"{settings.ORDER_SERVICE_URL}/orders",
            headers=headers
        )

        return response.json()


    @staticmethod
    def create_order(headers: dict):

        response = BaseHttpClient.post(
            url=f"{settings.ORDER_SERVICE_URL}/orders",
            headers=headers
        )

        return response.json()


    @staticmethod
    def get_order(order_id: int, headers: dict):

        response = BaseHttpClient.get(
            url=f"{settings.ORDER_SERVICE_URL}/orders/{order_id}",
            headers=headers
        )

        return response.json()


    @staticmethod
    def update_order_status(order_id: int, data: dict, headers: dict):

        response = BaseHttpClient.put(
            url=f"{settings.ORDER_SERVICE_URL}/orders/{order_id}/status",
            data=data,
            headers=headers
        )

        return response.json()
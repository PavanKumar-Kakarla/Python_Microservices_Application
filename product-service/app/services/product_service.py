from sqlalchemy.orm import Session

from app.core.exceptions import (
    ProductAlreadyExistsException,
    ProductNotFoundException
)
from app.core.logger import logger
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create_product(
        db: Session,
        product_data: ProductCreate
    ) -> Product:

        logger.info("Creating product: %s", product_data.name)

        existing_product = ProductRepository.get_product_by_sku(
            db,
            product_data.sku
        )

        if existing_product:
            raise ProductAlreadyExistsException()

        product = Product(**product_data.model_dump())

        return ProductRepository.create_product(
            db,
            product
        )

    @staticmethod
    def get_product(
        db: Session,
        product_id: int
    ) -> Product:

        logger.info("Fetching product: %s", product_id)

        product = ProductRepository.get_product_by_id(
            db,
            product_id
        )

        if not product:
            raise ProductNotFoundException()

        return product

    @staticmethod
    def get_all_products(
        db: Session
    ):

        logger.info("Fetching all products")

        return ProductRepository.get_all_products(db)

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate
    ) -> Product:

        logger.info("Updating product: %s", product_id)

        product = ProductRepository.get_product_by_id(
            db,
            product_id
        )

        if not product:
            raise ProductNotFoundException()

        if (
            product_data.sku is not None
            and product_data.sku != product.sku
        ):

            existing_product = ProductRepository.get_product_by_sku(
                db,
                product_data.sku
            )

            if existing_product:
                raise ProductAlreadyExistsException()

        for field, value in product_data.model_dump(
            exclude_unset=True
        ).items():

            setattr(product, field, value)

        return ProductRepository.update_product(
            db,
            product
        )

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int
    ):

        logger.info("Deleting product: %s", product_id)

        product = ProductRepository.get_product_by_id(
            db,
            product_id
        )

        if not product:
            raise ProductNotFoundException()

        ProductRepository.delete_product(
            db,
            product
        )
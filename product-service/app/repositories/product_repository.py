from sqlalchemy.orm import Session

from app.models.product import Product

from typing import List


class ProductRepository:

    @staticmethod
    def create_product(
        db: Session,
        product: Product
    ) -> Product:
        try:
            db.add(product)
            db.commit()
            db.refresh(product)

            return product

        except Exception:
            db.rollback()
            raise


    @staticmethod
    def get_product_by_id(
        db: Session,
        product_id: int
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )


    @staticmethod
    def get_product_by_sku(
        db: Session,
        sku: str
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(Product.sku == sku)
            .first()
        )


    @staticmethod
    def get_all_products(
        db: Session,
    ) -> List[Product]:

        return (
            db.query(Product).all()
        )


    @staticmethod
    def update_product(
        db: Session,
        product: Product
    ) -> Product:

        try:
            db.commit()
            db.refresh(product)

            return product

        except Exception:
            db.rollback()
            raise


    @staticmethod
    def delete_product(
        db: Session,
        product: Product
    ) -> None:

        try:
            db.delete(product)
            db.commit()

        except Exception:
            db.rollback()
            raise
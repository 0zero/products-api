from sqlalchemy.orm import Session

from src.database.crud.base import CRUDBase
from src.database.models.product import Product
from src.database.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """
    Product CRUD class with default methods to Create, Read, Update, Delete (CRUD).
    """
    
    def __init__(self, model: Product):
        super().__init__(model)

    def get_many_by_category(
        self, db: Session, category: str, skip: int = 0, limit: int = 100
    ) -> list[Product]:
        """
        Get many products by category

        input params:
            category -- The category of the product
            skip -- The number of records to skip
            limit -- The number of records to return
            db -- The database session

        return: A list of products
        """
        return (
            db.query(self.model)
            .filter(self.model.Category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_many_by_variety(
        self, db: Session, variety: str, skip: int = 0, limit: int = 100
    ) -> list[Product]:
        """
        Get many products by variety

        input params:
            variety -- The variety of the product
            skip -- The number of records to skip
            limit -- The number of records to return
            db -- The database session

        return: A list of products
        """
        return (
            db.query(self.model)
            .filter(self.model.Variety == variety)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_many_by_packaging(
        self, db: Session, packaging: str, skip: int = 0, limit: int = 100
    ) -> list[Product]:
        """
        Get many products by packaging

        input params:
            packaging -- The packaging of the product
            skip -- The number of records to skip
            limit -- The number of records to return
            db -- The database session

        return: A list of products
        """
        return (
            db.query(self.model)
            .filter(self.model.Packaging == packaging)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_many_by_category_and_variety_and_packaging(
        self,
        db: Session,
        category: str,
        variety: str,
        packaging: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        """
        Get many products by category, variety, and packaging

        input params:
            category -- The category of the product
            variety -- The variety of the product
            packaging -- The packaging of the product
            skip -- The number of records to skip
            limit -- The number of records to return
            db -- The database session

        return: A list of products
        """
        return (
            db.query(self.model)
            .filter(
                self.model.Category == category,
                self.model.Variety == variety,
                self.model.Packaging == packaging,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


# TODO: Add some logic to ensure we are properly validating the update

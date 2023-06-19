from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from src.database.crud.base import CRUDBase
from src.database.models.product import Product
from src.database.schemas.product import ProductCreate, ProductUpdate

# TODO: Add Get Many with filters


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def __init__(self, model: Product):
        super().__init__(model)

    def get_many_by_category(
        self, db: Session, category: str, skip: int = 0, limit: int = 100
    ) -> list[Product]:
        """
        Get many products by category
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

    def update(
        self,
        db: Session,
        db_obj: Product,
        obj_in: Union[ProductUpdate, Dict[str, Any]],
    ) -> Product:
        """Update a product ensuring we aren't setting nulls"""
        # TODO: Add some logic to ensure we are properly validating the update
        # before we contact the database
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

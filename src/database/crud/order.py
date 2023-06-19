from typing import Tuple

from sqlalchemy.orm import Session

from src.database.crud.base import CRUDBase
from src.database.crud.product import CRUDProduct
from src.database.models.order import Order
from src.database.models.product import Product
from src.database.schemas.order import OrderCreate, OrderUpdate
from src.database.schemas.product import ProductCreate

# TODO: Add Get Many with filters


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    """
    Orders CRUD class with default methods to Create, Read, Update, Delete (CRUD).
    """
    
    def __init__(self, model: Order):
        super().__init__(model)

    def create_new_order(
        self, db: Session, obj_in: OrderCreate
    ) -> Tuple[Order, list[int]]:
        """
        Create a new order in the database.
        For the list of products, iterate through them adding them to the Products table.


        Keyword arguments:
        db -- The database session
        obj_in -- The order object to create
        Return: The created order object
        """

        # Create the order
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Create the products
        product_ids = []
        product_crud = CRUDProduct(Product)  # type: ignore
        if obj_in.Products:
            for product in obj_in.Products:
                product_obj_in = ProductCreate(
                    Category=product.Category,
                    Variety=product.Variety,
                    Packaging=product.Packaging,
                )
                product_created = product_crud.create(db=db, obj_in=product_obj_in)
                product_ids.append(product_created.id)
        return db_obj, product_ids  # type: ignore

from src.database.crud.base import CRUDBase
from src.database.models.product import Product
from src.database.schemas.product import ProductDBBase, ProductCreate

from sqlalchemy.orm import Session


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductCreate]):
    def __init__(self, model: Product):
        super().__init__(model)

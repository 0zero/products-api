from src.database.crud.base import CRUDBase
from src.database.models.product import Product
from src.database.schemas.product import ProductDBBase

from sqlalchemy.orm import Session

class CRUDProduct(CRUDBase):
    def __init__(self, model: Product):
        super().__init__(model)

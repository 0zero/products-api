from src.database.crud.base import CRUDBase
from src.database.models.product import Product
from src.database.schemas.product import ProductCreate, ProductUpdate

# TODO: Add Get Many with filters


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def __init__(self, model: Product):
        super().__init__(model)

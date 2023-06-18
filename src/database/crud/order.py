from src.database.crud.base import CRUDBase
from src.database.models.order import Order, ProductType
from src.database.schemas.order import OrderDBBase, ProductOrderType
from src.database.models.base import OrderTypeEnum

from sqlalchemy.orm import Session

class CRUDOrder(CRUDBase):
    def __init__(self, model: Order):
        super().__init__(model)

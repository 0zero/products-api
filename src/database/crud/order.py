from src.database.crud.base import CRUDBase
from src.database.models.order import Order, ProductType
from src.database.schemas.order import OrderDBBase, ProductOrderType, OrderCreate
from src.database.models.base import OrderTypeEnum

from sqlalchemy.orm import Session


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderCreate]):
    def __init__(self, model: Order):
        super().__init__(model)

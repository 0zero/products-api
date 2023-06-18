from sqlalchemy.orm import Session

from src.database.crud.base import CRUDBase
from src.database.models.base import OrderTypeEnum
from src.database.models.order import Order, ProductType
from src.database.schemas.order import OrderCreate, OrderDBBase, ProductOrderType


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderCreate]):
    def __init__(self, model: Order):
        super().__init__(model)

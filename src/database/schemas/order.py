from typing import List, Optional

from pydantic import BaseModel

from src.database.models.base import OrderTypeEnum


class ProductOrderType(BaseModel):
    Category: str
    Variety: str
    Packaging: str
    Volume: str
    Price_per_unit: str


class OrderDBBase(BaseModel):
    id: int
    Type: OrderTypeEnum
    References: Optional[int]
    Products: List[ProductOrderType]
    Organisation_id: int

    class Config:
        orm_mode = True

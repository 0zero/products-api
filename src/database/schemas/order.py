from typing import List, Optional

from pydantic import BaseModel

from src.database.models.base import OrderTypeEnum


class ProductOrderType(BaseModel):
    Category: str
    Variety: str
    Packaging: str
    Volume: str
    Price_per_unit: str


class OrderBase(BaseModel):
    Type: Optional[OrderTypeEnum]
    References: Optional[int]
    Products: Optional[List[ProductOrderType]]
    Organisation_id: Optional[int]


class OrderCreate(OrderBase):
    Type: OrderTypeEnum
    References: Optional[int]
    Products: List[ProductOrderType]
    Organisation_id: int


class OrderUpdate(OrderBase):
    Type: Optional[OrderTypeEnum]
    References: Optional[int]
    Products: Optional[List[ProductOrderType]]
    Organisation_id: Optional[int]


class OrderDBBase(OrderBase):
    id: int
    Organisation_id: int

    class Config:
        orm_mode = True

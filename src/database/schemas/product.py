from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    Category: Optional[str]
    Variety: Optional[str]
    Packaging: Optional[str]


class ProductCreate(ProductBase):
    Category: str
    Variety: str
    Packaging: str


class ProductUpdate(ProductBase):
    Category: Optional[str]
    Variety: Optional[str]
    Packaging: Optional[str]


class ProductDBBase(ProductBase):
    id: int

    class Config:
        orm_mode = True

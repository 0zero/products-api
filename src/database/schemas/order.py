from typing import Dict, List, Optional

from pydantic import BaseModel

from src.database.models.base import OrderTypeEnum


class ProductOrderType(BaseModel):
    Category: str
    Variety: str
    Packaging: str
    Volume: str
    Price_per_unit: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "Category": self.Category,
            "Variety": self.Variety,
            "Packaging": self.Packaging,
            "Volume": self.Volume,
            "Price_per_unit": self.Price_per_unit,
        }


class OrderDBBase(BaseModel):
    id: int
    Type: OrderTypeEnum
    References: Optional[int]
    Products: List[ProductOrderType]
    Organisation_id: int

    class Config:
        orm_mode = True

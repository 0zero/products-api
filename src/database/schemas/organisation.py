from typing import Optional

from pydantic import BaseModel

from src.database.models.base import OrganisationTypeEnum
from src.database.schemas.order import OrderDBBase, ProductOrderType


class OrganisationBase(BaseModel):
    Name: Optional[str]
    Type: Optional[OrganisationTypeEnum]


class OrganisationCreate(OrganisationBase):
    Name: str
    Type: Optional[OrganisationTypeEnum]


class OrganisationUpdate(OrganisationBase):
    Name: Optional[str]
    Type: Optional[OrganisationTypeEnum]


class OrganisationDBBase(OrganisationBase):
    id: int
    Orders: list[OrderDBBase]
    Products: list[ProductOrderType]

    class Config:
        orm_mode = True

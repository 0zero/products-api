from enum import Enum

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderTypeEnum(str, Enum):
    BUY: str = "BUY"
    SELL: str = "SELL"


class OrganisationTypeEnum(str, Enum):
    BUYER: str = "BUYER"
    SELLER: str = "SELLER"

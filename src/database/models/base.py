from enum import Enum

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderTypeEnum(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrganisationTypeEnum(Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"

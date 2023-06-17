from enum import Enum

import sqlalchemy as sqla
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# TODO: Use Mapped and mapped_column to declare models instead of declarative_base
# see https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models


class ProductType(sqla.types.TypeDecorator):  # type: ignore
    impl = sqla.types.String

    def process_bind_param(self, value, dialect):  # type: ignore
        if value is not None:
            return (
                f"{value['Category']},{value['Variety']},{value['Packaging']},"
                f"{value['Volume']},{value['Price_per_unit']}"
            )
        return None

    def process_result_value(self, value, dialect):  # type: ignore
        if value is not None:
            category, variety, packaging, volume, price_per_unit = value.split(",")
            return {
                "Category": category,
                "Variety": variety,
                "Packaging": packaging,
                "Volume": volume,
                "Price_per_unit": float(price_per_unit),
            }
        return None


class OrderTypeEnum(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrganisationTypeEnum(Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"


# Classes used for database table


class Product(Base):  # type: ignore
    __tablename__ = "products"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    Category = sqla.Column(sqla.String, index=True, nullable=False)
    Variety = sqla.Column(sqla.String, nullable=False)
    Packaging = sqla.Column(sqla.String, nullable=False)


class Order(Base):  # type: ignore
    __tablename__ = "orders"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    Type = sqla.Column(sqla.Enum(OrderTypeEnum), index=True, nullable=False)  # type: ignore
    References = sqla.Column(sqla.Integer, sqla.ForeignKey("orders.id"))
    Products = sqla.Column(sqla.ARRAY(ProductType), nullable=False)  # type: ignore
    Organisation_id = sqla.Column(sqla.Integer, sqla.ForeignKey("organisations.id"))
    Organization = sqla.relationship("Organisation", backref="orders")  # type: ignore


class Organisation(Base):  # type: ignore
    __tablename__ = "organisations"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    Name = sqla.Column(sqla.String, unique=True, index=True, nullable=False)
    Type = sqla.Column(sqla.Enum(OrganisationTypeEnum), index=True, nullable=True)  # type: ignore
    Products = sqla.relationship("Order")  # type: ignore
    Orders = sqla.relationship("Order")  # type: ignore

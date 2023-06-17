import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from src.database.models.base import Base, OrderTypeEnum
from src.database.models.organisation import Organisation  # noqa: F401

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
                "Price_per_unit": price_per_unit,
            }
        return None


# Classes used for database table


class Order(Base):
    __tablename__ = "orders"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    Type = sqla.Column(sqla.Enum(OrderTypeEnum), index=True, nullable=False)  # type: ignore
    References = sqla.Column(sqla.Integer, sqla.ForeignKey("orders.id"))
    Products = sqla.Column(sqla.ARRAY(ProductType), nullable=False)  # type: ignore
    Organisation_id = sqla.Column(sqla.Integer, sqla.ForeignKey("organisations.id"))
    Organization = relationship("Organisation", backref="orders")

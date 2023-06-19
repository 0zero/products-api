from typing import Any

import sqlalchemy as sqla
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from src.database.models.base import Base, OrganisationTypeEnum

# TODO: Use Mapped and mapped_column to declare models instead of declarative_base
# see https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models


# Classes used for database table


class Organisation(Base):
    __tablename__ = "organisations"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    Name = sqla.Column(sqla.String, unique=True, index=True, nullable=False)
    Type = sqla.Column(sqla.Enum(OrganisationTypeEnum), index=True, nullable=True)  # type: ignore
    Orders = relationship("Order")

    @hybrid_property
    def Products(self) -> list[dict[str, Any]]:
        return [product for order in self.Orders for product in order.Products]

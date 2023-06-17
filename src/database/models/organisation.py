import sqlalchemy as sqla
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
    Products = relationship("Order")
    Orders = relationship("Order")

import sqlalchemy as sqla

from src.database.models.base import Base

# TODO: Use Mapped and mapped_column to declare models instead of declarative_base
# see https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models


# Classes used for database table


class Product(Base):
    __tablename__ = "products"

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    Category = sqla.Column(sqla.String, index=True, nullable=False)
    Variety = sqla.Column(sqla.String, nullable=False)
    Packaging = sqla.Column(sqla.String, nullable=False)

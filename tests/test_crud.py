import pytest
from sqlalchemy.orm import Session

from src.database.crud.order import CRUDOrder
from src.database.crud.organisation import CRUDOrganisation
from src.database.crud.product import CRUDProduct
from src.database.models.base import OrderTypeEnum, OrganisationTypeEnum
from src.database.models.order import Order, ProductType
from src.database.models.organisation import Organisation
from src.database.models.product import Product
from src.database.schemas.order import OrderCreate, ProductOrderType
from src.database.schemas.organisation import OrganisationCreate
from src.database.schemas.product import ProductCreate


def test_create_product(test_db: Session) -> None:
    product = ProductCreate(
        Category="test category", Variety="test variety", Packaging="test packaging"
    )
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=product)
    assert product_creacted.id is not None
    assert product_creacted.Category == "test category"
    assert product_creacted.Variety == "test variety"
    assert product_creacted.Packaging == "test packaging"

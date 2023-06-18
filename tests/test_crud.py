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


def test_get_product(test_db: Session) -> None:
    product = ProductCreate(
        Category="test category", Variety="test variety", Packaging="test packaging"
    )
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=product)
    product_get = product_crud.get(db=test_db, id=product_creacted.id)
    assert product_get.id is not None
    assert product_get.Category == "test category"
    assert product_get.Variety == "test variety"
    assert product_get.Packaging == "test packaging"


def test_get_many_products(test_db: Session) -> None:
    product1 = ProductCreate(
        Category="test category1", Variety="test variety1", Packaging="test packaging1"
    )
    product2 = ProductCreate(
        Category="test category2", Variety="test variety2", Packaging="test packaging2"
    )
    product_crud = CRUDProduct(Product)
    product_creacted1 = product_crud.create(db=test_db, obj_in=product1)
    product_creacted2 = product_crud.create(db=test_db, obj_in=product2)
    product_get_many = product_crud.get_multi(db=test_db)
    assert len(product_get_many) > 1
    assert product_get_many[-2].id is not None
    assert product_get_many[-2].Category == product_creacted1.Category
    assert product_get_many[-2].Variety == product_creacted1.Variety
    assert product_get_many[-2].Packaging == product_creacted1.Packaging
    assert product_get_many[-1].id is not None
    assert product_get_many[-1].Category == product_creacted2.Category
    assert product_get_many[-1].Variety == product_creacted2.Variety
    assert product_get_many[-1].Packaging == product_creacted2.Packaging


def test_update_product(test_db: Session) -> None:
    product = ProductCreate(
        Category="test category", Variety="test variety", Packaging="test packaging"
    )
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=product)
    product_update = ProductCreate(
        Category="test category 2",
        Variety="test variety 2",
        Packaging="test packaging 2",
    )
    product_updated = product_crud.update(
        db=test_db, db_obj=product_creacted, obj_in=product_update
    )
    assert product_updated.id is not None
    assert product_updated.Category == "test category 2"
    assert product_updated.Variety == "test variety 2"
    assert product_updated.Packaging == "test packaging 2"


def test_delete_product(test_db: Session) -> None:
    product = ProductCreate(
        Category="test category", Variety="test variety", Packaging="test packaging"
    )
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=product)
    product_deleted = product_crud.remove(db=test_db, id=product_creacted.id)
    product_get = product_crud.get(db=test_db, id=product_creacted.id)
    assert product_deleted.id is not None
    assert product_deleted.Category == "test category"
    assert product_deleted.Variety == "test variety"
    assert product_deleted.Packaging == "test packaging"
    assert product_get is None

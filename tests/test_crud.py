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


@pytest.fixture()
def test_product_one() -> ProductCreate:
    return ProductCreate(
        Category="test category 1",
        Variety="test variety 1",
        Packaging="test packaging 1",
    )


@pytest.fixture()
def test_product_two() -> ProductCreate:
    return ProductCreate(
        Category="test category 2",
        Variety="test variety 2",
        Packaging="test packaging 2",
    )


@pytest.fixture()
def test_product_three() -> ProductCreate:
    return ProductCreate(
        Category="test category 3",
        Variety="test variety 3",
        Packaging="test packaging 3",
    )


@pytest.fixture()
def test_order_one_no_references(test_product_one: ProductCreate) -> OrderCreate:
    return OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=[test_product_one],
        Organisation_id=1,
    )


@pytest.fixture()
def test_order_two_with_references(
    test_product_one: ProductCreate, test_product_two: ProductCreate
) -> OrderCreate:
    return OrderCreate(
        Type=OrderTypeEnum.BUY,
        References=1,
        Products=[test_product_one, test_product_two],
        Organisation_id=1,
    )


@pytest.fixture()
def test_organisation_one() -> OrganisationCreate:
    return OrganisationCreate(
        Name="test organisation 1",
        Type=OrganisationTypeEnum.BUYER,
    )


@pytest.fixture()
def test_organisation_two() -> OrganisationCreate:
    return OrganisationCreate(
        Name="test organisation 2",
        Type=OrganisationTypeEnum.BUYER,
    )


def test_create_product(test_db: Session, test_product_one: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=test_product_one)
    assert product_creacted.id is not None
    assert product_creacted.Category == test_product_one.Category
    assert product_creacted.Variety == test_product_one.Variety
    assert product_creacted.Packaging == test_product_one.Packaging


def test_get_product(test_db: Session, test_product_two: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=test_product_two)
    product_get = product_crud.get(db=test_db, id=product_creacted.id)
    assert product_get.id == product_creacted.id
    assert product_get.Category == test_product_two.Category
    assert product_get.Variety == test_product_two.Variety
    assert product_get.Packaging == test_product_two.Packaging


def test_get_many_products(
    test_db: Session, test_product_two: ProductCreate, test_product_three: ProductCreate
) -> None:
    product_crud = CRUDProduct(Product)
    product_creacted2 = product_crud.create(db=test_db, obj_in=test_product_two)
    product_creacted3 = product_crud.create(db=test_db, obj_in=test_product_three)
    product_get_many = product_crud.get_multi(db=test_db)
    assert len(product_get_many) > 1
    assert product_get_many[-2].id == product_creacted2.id
    assert product_get_many[-2].Category == test_product_two.Category
    assert product_get_many[-2].Variety == test_product_two.Variety
    assert product_get_many[-2].Packaging == test_product_two.Packaging
    assert product_get_many[-1].id == product_creacted3.id
    assert product_get_many[-1].Category == test_product_three.Category
    assert product_get_many[-1].Variety == test_product_three.Variety
    assert product_get_many[-1].Packaging == test_product_three.Packaging


def test_update_product(test_db: Session, test_product_one: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=test_product_one)
    product_update = ProductCreate(
        Category="test category updated",
        Variety="test variety updated",
        Packaging="test packaging updated",
    )
    product_updated = product_crud.update(
        db=test_db, db_obj=product_creacted, obj_in=product_update
    )
    assert product_updated.id == product_creacted.id
    assert product_updated.Category == product_update.Category
    assert product_updated.Variety == product_update.Variety
    assert product_updated.Packaging == product_update.Packaging


def test_delete_product(test_db: Session, test_product_three: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_creacted = product_crud.create(db=test_db, obj_in=test_product_three)
    product_deleted = product_crud.remove(db=test_db, id=product_creacted.id)
    product_get = product_crud.get(db=test_db, id=product_creacted.id)
    assert product_deleted.id == product_creacted.id
    assert product_deleted.Category == test_product_three.Category
    assert product_deleted.Variety == test_product_three.Variety
    assert product_deleted.Packaging == test_product_three.Packaging
    assert product_get is None

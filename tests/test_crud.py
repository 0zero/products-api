from typing import List

import pytest
from sqlalchemy.orm import Session
from tests.helpers import get_random_string

from src.database.crud.order import CRUDOrder
from src.database.crud.organisation import CRUDOrganisation
from src.database.crud.product import CRUDProduct
from src.database.models.base import OrderTypeEnum, OrganisationTypeEnum
from src.database.models.order import Order
from src.database.models.organisation import Organisation
from src.database.models.product import Product
from src.database.schemas.order import OrderCreate, OrderUpdate, ProductOrderType
from src.database.schemas.organisation import OrganisationCreate, OrganisationUpdate
from src.database.schemas.product import ProductCreate, ProductUpdate


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
def test_product_order_type_list_of_one(
    test_product_one: ProductCreate,
) -> List[ProductOrderType]:
    return [
        ProductOrderType(
            Category=test_product_one.Category,
            Variety=test_product_one.Variety,
            Packaging=test_product_one.Packaging,
            Volume="test volume 1",
            Price_per_unit="test price per unit 1",
        )
    ]


@pytest.fixture()
def test_product_order_type_list_of_two(
    test_product_one: ProductCreate, test_product_two: ProductCreate
) -> List[ProductOrderType]:
    product_order_one = ProductOrderType(
        Category=test_product_one.Category,
        Variety=test_product_one.Variety,
        Packaging=test_product_one.Packaging,
        Volume="test volume 1",
        Price_per_unit="test price per unit 1",
    )
    product_order_two = ProductOrderType(
        Category=test_product_two.Category,
        Variety=test_product_two.Variety,
        Packaging=test_product_two.Packaging,
        Volume="test volume 2",
        Price_per_unit="test price per unit 2",
    )
    return [product_order_one, product_order_two]


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


@pytest.fixture()
def test_organisation_three() -> OrganisationCreate:
    return OrganisationCreate(
        Name="test organisation 3",
        Type=OrganisationTypeEnum.BUYER,
    )


# TODO: Test some failure scenarios

# TEST PRODUCT CRUD


def test_create_product(test_db: Session, test_product_one: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_created = product_crud.create(db=test_db, obj_in=test_product_one)
    assert product_created.id is not None
    assert product_created.Category == test_product_one.Category
    assert product_created.Variety == test_product_one.Variety
    assert product_created.Packaging == test_product_one.Packaging


def test_read_product(test_db: Session, test_product_two: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_created = product_crud.create(db=test_db, obj_in=test_product_two)
    product_get = product_crud.get(db=test_db, id=product_created.id)
    assert product_get.id == product_created.id
    assert product_get.Category == test_product_two.Category
    assert product_get.Variety == test_product_two.Variety
    assert product_get.Packaging == test_product_two.Packaging


def test_read_many_products(
    test_db: Session, test_product_two: ProductCreate, test_product_three: ProductCreate
) -> None:
    product_crud = CRUDProduct(Product)
    product_created2 = product_crud.create(db=test_db, obj_in=test_product_two)
    product_created3 = product_crud.create(db=test_db, obj_in=test_product_three)
    product_get_many = product_crud.get_multi(db=test_db)
    assert len(product_get_many) > 1
    assert product_get_many[-2].id == product_created2.id
    assert product_get_many[-2].Category == test_product_two.Category
    assert product_get_many[-2].Variety == test_product_two.Variety
    assert product_get_many[-2].Packaging == test_product_two.Packaging
    assert product_get_many[-1].id == product_created3.id
    assert product_get_many[-1].Category == test_product_three.Category
    assert product_get_many[-1].Variety == test_product_three.Variety
    assert product_get_many[-1].Packaging == test_product_three.Packaging


def test_update_product(test_db: Session, test_product_one: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_created = product_crud.create(db=test_db, obj_in=test_product_one)
    product_update = ProductUpdate(
        Packaging="test packaging updated",
    )
    product_updated = product_crud.update(
        db=test_db, db_obj=product_created, obj_in=product_update
    )
    assert product_updated.id == product_created.id
    assert product_updated.Category == product_created.Category
    assert product_updated.Variety == product_created.Variety
    assert product_updated.Packaging == product_update.Packaging


def test_delete_product(test_db: Session, test_product_three: ProductCreate) -> None:
    product_crud = CRUDProduct(Product)
    product_created = product_crud.create(db=test_db, obj_in=test_product_three)
    product_deleted = product_crud.remove(db=test_db, id=product_created.id)
    product_get = product_crud.get(db=test_db, id=product_created.id)
    assert product_deleted.id == product_created.id
    assert product_deleted.Category == test_product_three.Category
    assert product_deleted.Variety == test_product_three.Variety
    assert product_deleted.Packaging == test_product_three.Packaging
    assert product_get is None


# TEST ORGANISATION CRUD


def test_create_organisation(
    test_db: Session, test_organisation_one: OrganisationCreate
) -> None:
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(
        db=test_db, obj_in=test_organisation_one
    )
    assert organisation_created.id is not None
    assert organisation_created.Name == test_organisation_one.Name
    assert organisation_created.Type == test_organisation_one.Type


def test_create_organisation_with_no_type(test_db: Session) -> None:
    organisation_one = OrganisationCreate(Name=get_random_string())

    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(db=test_db, obj_in=organisation_one)
    assert organisation_created.id is not None
    assert organisation_created.Name == organisation_one.Name
    assert organisation_created.Type is None


def test_read_organisation(
    test_db: Session, test_organisation_two: OrganisationCreate
) -> None:
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(
        db=test_db, obj_in=test_organisation_two
    )
    organisation_read = organisation_crud.get(db=test_db, id=organisation_created.id)
    assert organisation_read.id == organisation_created.id
    assert organisation_read.Name == test_organisation_two.Name
    assert organisation_read.Type == test_organisation_two.Type


def test_read_many_organisations(test_db: Session) -> None:
    organisation_one = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_two = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.SELLER
    )

    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created_one = organisation_crud.create(
        db=test_db, obj_in=organisation_one
    )
    organisation_created_two = organisation_crud.create(
        db=test_db, obj_in=organisation_two
    )
    organisation_read_many = organisation_crud.get_multi(db=test_db)
    assert len(organisation_read_many) > 1
    assert organisation_read_many[-2].id == organisation_created_one.id
    assert organisation_read_many[-2].Name == organisation_one.Name
    assert organisation_read_many[-2].Type == organisation_one.Type
    assert organisation_read_many[-1].id == organisation_created_two.id
    assert organisation_read_many[-1].Name == organisation_two.Name
    assert organisation_read_many[-1].Type == organisation_two.Type


def test_remove_organisation(
    test_db: Session, test_organisation_three: OrganisationCreate
) -> None:
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(
        db=test_db, obj_in=test_organisation_three
    )
    organisation_deleted = organisation_crud.remove(
        db=test_db, id=organisation_created.id
    )
    organisation_get = organisation_crud.get(db=test_db, id=organisation_created.id)
    assert organisation_deleted.id == organisation_created.id
    assert organisation_deleted.Name == test_organisation_three.Name
    assert organisation_deleted.Type == test_organisation_three.Type
    assert organisation_get is None


def test_update_organisation(test_db: Session) -> None:
    organisation_one = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(db=test_db, obj_in=organisation_one)

    organisation_update = OrganisationUpdate(
        Type=OrganisationTypeEnum.SELLER,
    )
    organisation_updated = organisation_crud.update(
        db=test_db, db_obj=organisation_created, obj_in=organisation_update
    )
    assert organisation_updated.id == organisation_created.id
    assert organisation_updated.Name == organisation_created.Name
    assert organisation_updated.Type == organisation_update.Type


# TEST ORDER CRUD


def test_create_order_with_no_references(
    test_db: Session,
    test_product_order_type_list_of_one: List[ProductOrderType],
) -> None:
    # Create organisation
    organisation_one = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(db=test_db, obj_in=organisation_one)
    assert organisation_created.id is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_one,
        Organisation_id=organisation_created.id,
    )

    order_crud = CRUDOrder(Order)
    order_created, product_ids_created = order_crud.create_new_order(
        db=test_db, obj_in=order_in
    )
    assert order_created
    assert product_ids_created
    assert len(product_ids_created) == 1

    assert order_created.id is not None
    assert order_created.Type == order_in.Type
    assert order_created.Organisation_id == organisation_created.id
    assert len(order_created.Products) == 1
    test_product_type = test_product_order_type_list_of_one[0]
    assert order_created.Products[0]["Category"] == test_product_type.Category
    assert order_created.Products[0]["Variety"] == test_product_type.Variety
    assert order_created.Products[0]["Packaging"] == test_product_type.Packaging

    # Check whether product got added to products table
    product_crud = CRUDProduct(Product)
    product_get = product_crud.get(db=test_db, id=product_ids_created[0])
    assert product_get.id == product_ids_created[0]


def test_create_order_with_references(
    test_db: Session,
    test_product_order_type_list_of_two: List[ProductOrderType],
) -> None:
    organisation_one = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(db=test_db, obj_in=organisation_one)
    assert organisation_created.id is not None

    order_crud = CRUDOrder(Order)

    reference_order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_created.id,
    )
    (
        reference_order_created,
        reference_product_ids_created,
    ) = order_crud.create_new_order(db=test_db, obj_in=reference_order_in)
    assert reference_order_created.id is not None
    assert reference_product_ids_created
    assert len(reference_product_ids_created) == 2

    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_created.id,
        References=reference_order_created.id,
    )
    order_created, product_ids_created = order_crud.create_new_order(
        db=test_db, obj_in=order_in
    )
    assert order_created
    assert product_ids_created
    assert len(product_ids_created) == 2

    assert order_created.id is not None
    assert order_created.Type == order_in.Type
    assert order_created.Organisation_id == organisation_created.id
    assert order_created.References == reference_order_created.id
    assert len(order_created.Products) == 2
    test_product_type_one = test_product_order_type_list_of_two[0]
    test_product_type_two = test_product_order_type_list_of_two[1]
    assert order_created.Products[0]["Category"] == test_product_type_one.Category
    assert order_created.Products[1]["Category"] == test_product_type_two.Category

    # Check whether product got added to products table
    product_crud = CRUDProduct(Product)
    product_get_first_product = product_crud.get(db=test_db, id=product_ids_created[0])
    product_get_second_product = product_crud.get(db=test_db, id=product_ids_created[1])
    assert product_get_first_product.id == product_ids_created[0]
    assert product_get_second_product.id == product_ids_created[1]


def test_read_order(
    test_db: Session, test_product_order_type_list_of_one: List[ProductOrderType]
) -> None:
    # Create organisation
    organisation_one = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(db=test_db, obj_in=organisation_one)
    assert organisation_created.id is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_one,
        Organisation_id=organisation_created.id,
    )

    order_crud = CRUDOrder(Order)
    order_created, product_ids_created = order_crud.create_new_order(
        db=test_db, obj_in=order_in
    )
    assert order_created
    assert product_ids_created

    order_get = order_crud.get(db=test_db, id=order_created.id)
    assert order_get.id == order_created.id
    assert order_get.Type == order_created.Type
    assert order_get.Organisation_id == order_created.Organisation_id
    assert order_get.References == order_created.References
    assert order_get.Products == order_created.Products


def test_update_order(
    test_db: Session, test_product_order_type_list_of_one: List[ProductOrderType]
) -> None:
    # Create organisation
    organisation_one = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(db=test_db, obj_in=organisation_one)
    assert organisation_created.id is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_one,
        Organisation_id=organisation_created.id,
    )

    order_crud = CRUDOrder(Order)
    order_created, product_ids_created = order_crud.create_new_order(
        db=test_db, obj_in=order_in
    )
    assert order_created
    assert product_ids_created
    # Update order
    order_update = OrderUpdate(
        Type=OrderTypeEnum.BUY,
    )
    order_updated = order_crud.update(
        db=test_db, db_obj=order_created, obj_in=order_update
    )
    assert order_updated.id == order_created.id
    assert order_updated.Type == order_update.Type
    assert order_updated.Organisation_id == order_created.Organisation_id
    assert order_updated.References == order_created.References


def test_delete_order(
    test_db: Session, test_product_order_type_list_of_one: List[ProductOrderType]
) -> None:
    # Create organisation
    organisation_one = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_crud = CRUDOrganisation(Organisation)
    organisation_created = organisation_crud.create(db=test_db, obj_in=organisation_one)
    assert organisation_created.id is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_one,
        Organisation_id=organisation_created.id,
    )

    order_crud = CRUDOrder(Order)
    order_created, product_ids_created = order_crud.create_new_order(
        db=test_db, obj_in=order_in
    )
    assert order_created
    assert product_ids_created
    # Delete order
    order_deleted = order_crud.remove(db=test_db, id=order_created.id)
    order_get = order_crud.get(db=test_db, id=order_created.id)

    assert order_deleted.id == order_created.id
    assert order_deleted.Type == order_created.Type
    assert order_deleted.Organisation_id == order_created.Organisation_id
    assert order_deleted.References == order_created.References
    assert order_get is None


# TODO: TEST fully coupled example

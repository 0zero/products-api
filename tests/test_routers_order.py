from typing import List

import pytest
from fastapi.testclient import TestClient
from tests.helpers import get_random_string

from src.database.models.base import OrderTypeEnum, OrganisationTypeEnum
from src.database.schemas.order import OrderCreate, OrderUpdate, ProductOrderType
from src.database.schemas.organisation import OrganisationCreate


@pytest.fixture()
def test_product_order_type_list_of_two() -> List[ProductOrderType]:
    product_order_one = ProductOrderType(
        Category="test category 1",
        Variety="test variety 1",
        Packaging="test packaging 1",
        Volume="test volume 1",
        Price_per_unit="test price per unit 1",
    )
    product_order_two = ProductOrderType(
        Category="test category 2",
        Variety="test variety 2",
        Packaging="test packaging 2",
        Volume="test volume 2",
        Price_per_unit="test price per unit 2",
    )
    return [product_order_one, product_order_two]


def test_successful_post_single_order_without_references(
    test_app_with_db: TestClient,
    test_product_order_type_list_of_two: List[ProductOrderType],
) -> None:
    # Create organisation
    organisation_in = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )

    assert organisation_response.status_code == 201

    organisation_content = organisation_response.json()
    assert organisation_content["id"] is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_content["id"],
    )
    order_response = test_app_with_db.post("/api/order", json=order_in.dict())

    assert order_response.status_code == 201

    order_content = order_response.json()
    assert order_content["id"] is not None
    assert order_content["Type"] == order_in.Type
    assert order_content["Products"] == order_in.Products
    assert order_content["Organisation_id"] == organisation_content["id"]


def test_successful_post_single_order_with_references(
    test_app_with_db: TestClient,
    test_product_order_type_list_of_two: List[ProductOrderType],
) -> None:
    # Create organisation
    organisation_in = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert organisation_response.status_code == 201
    organisation_content = organisation_response.json()
    assert organisation_content["id"] is not None

    # Create Referenced Order
    order_ref = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_content["id"],
    )
    ref_response = test_app_with_db.post("/api/order", json=order_ref.dict())
    assert ref_response.status_code == 201

    ref_content = ref_response.json()
    assert ref_content["id"] is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.BUY,
        Organisation_id=organisation_content["id"],
        References=ref_content["id"],
    )
    order_response = test_app_with_db.post("/api/order", json=order_in.dict())
    assert order_response.status_code == 201

    order_content = order_response.json()
    assert order_content["id"] is not None
    assert order_content["Type"] == order_in.Type
    assert order_content["Products"] == order_ref.Products
    assert order_content["Organisation_id"] == organisation_content["id"]
    assert order_content["References"] == ref_content["id"]


def test_failure_to_post_single_order(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post("/api/order", json=dict())

    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "Type"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "Organisation_id"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_successful_get_single_order(
    test_app_with_db: TestClient,
    test_product_order_type_list_of_two: List[ProductOrderType],
) -> None:
    # Create organisation
    organisation_in = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert organisation_response.status_code == 201
    organisation_content = organisation_response.json()
    assert organisation_content["id"] is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_content["id"],
    )
    post_response = test_app_with_db.post("/api/order", json=order_in.dict())
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    # Get order
    get_response = test_app_with_db.get(f"/api/order/{post_content['id']}")

    assert get_response.status_code == 200

    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Type"] == order_in.Type
    assert get_content["Products"] == order_in.Products
    assert get_content["Organisation_id"] == organisation_content["id"]


def test_order_not_found_to_get(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.get("/api/order/999")
    assert response.status_code == 404

    assert response.json() == {"detail": "order not found"}


def test_unsuccessful_get_single_order(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.get("/api/order/one")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "order_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_successful_delete_single_order(
    test_app_with_db: TestClient,
    test_product_order_type_list_of_two: List[ProductOrderType],
) -> None:
    # Create organisation
    organisation_in = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert organisation_response.status_code == 201
    organisation_content = organisation_response.json()
    assert organisation_content["id"] is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_content["id"],
    )
    post_response = test_app_with_db.post("/api/order", json=order_in.dict())
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    # Delete order
    delete_response = test_app_with_db.delete(f"/api/order/{post_content['id']}")

    assert delete_response.status_code == 200

    delete_content = delete_response.json()
    assert delete_content["id"] == post_content["id"]
    assert delete_content["Type"] == order_in.Type
    assert delete_content["Products"] == order_in.Products
    assert delete_content["Organisation_id"] == organisation_content["id"]

    get_response = test_app_with_db.get(f"/api/order/{post_content['id']}")
    assert get_response.status_code == 404


def test_unsuccessful_delete_single_order(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.delete("/api/order/{345}")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "order_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_successful_update_single_order(
    test_app_with_db: TestClient,
    test_product_order_type_list_of_two: List[ProductOrderType],
) -> None:
    # Create organisation
    organisation_in = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert organisation_response.status_code == 201
    organisation_content = organisation_response.json()
    assert organisation_content["id"] is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_content["id"],
    )
    post_response = test_app_with_db.post("/api/order", json=order_in.dict())
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    # Update order
    order_update = OrderUpdate(
        Type=OrderTypeEnum.BUY,
    )
    update_response = test_app_with_db.put(
        f"/api/order/{post_content['id']}", json=order_update.dict(exclude_unset=True)
    )

    assert update_response.status_code == 201

    update_content = update_response.json()
    assert update_content["id"] == post_content["id"]
    assert update_content["Type"] == order_update.Type
    assert update_content["Products"] == order_in.Products
    assert update_content["Organisation_id"] == organisation_content["id"]

    get_response = test_app_with_db.get(f"/api/order/{post_content['id']}")
    assert get_response.status_code == 200
    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Type"] == order_update.Type


def test_unsuccessful_update_single_order(
    test_app_with_db: TestClient,
    test_product_order_type_list_of_two: List[ProductOrderType],
) -> None:
    # Create organisation
    organisation_in = OrganisationCreate(
        Name=get_random_string(), Type=OrganisationTypeEnum.BUYER
    )
    organisation_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert organisation_response.status_code == 201
    organisation_content = organisation_response.json()
    assert organisation_content["id"] is not None

    # Create order
    order_in = OrderCreate(
        Type=OrderTypeEnum.SELL,
        Products=test_product_order_type_list_of_two,
        Organisation_id=organisation_content["id"],
    )
    post_response = test_app_with_db.post("/api/order", json=order_in.dict())
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    # Update order
    order_update = OrderUpdate()
    update_response = test_app_with_db.put(
        "/api/order/two", json=order_update.dict(exclude_unset=True)
    )
    assert update_response.status_code == 422
    assert update_response.json() == {
        "detail": [
            {
                "loc": ["path", "order_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }

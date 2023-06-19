import pytest
from fastapi.testclient import TestClient

from src.database.schemas.product import ProductCreate, ProductUpdate


@pytest.fixture()
def test_product_one() -> ProductCreate:
    return ProductCreate(
        Category="test category 1",
        Variety="test variety 1",
        Packaging="test packaging 1",
    )


def test_successful_post_single_product(
    test_app_with_db: TestClient, test_product_one: ProductCreate
) -> None:
    response = test_app_with_db.post("/api/product", json=test_product_one.dict())

    assert response.status_code == 201

    content = response.json()
    assert content["id"] is not None
    assert content["Category"] == test_product_one.Category
    assert content["Variety"] == test_product_one.Variety
    assert content["Packaging"] == test_product_one.Packaging


def test_failure_to_post_single_product(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post("/api/product", json=dict())

    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "Category"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "Variety"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "Packaging"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_successful_get_single_product(
    test_app_with_db: TestClient, test_product_one: ProductCreate
) -> None:
    post_response = test_app_with_db.post("/api/product", json=test_product_one.dict())

    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    get_response = test_app_with_db.get(f"/api/product/{post_content['id']}")

    assert get_response.status_code == 200

    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Category"] == test_product_one.Category
    assert get_content["Variety"] == test_product_one.Variety
    assert get_content["Packaging"] == test_product_one.Packaging


def test_unsuccessful_get_single_product(test_app_with_db: TestClient) -> None:
    get_response = test_app_with_db.get(f"/api/product/{5.4}")
    assert get_response.status_code == 422
    assert get_response.json() == {
        "detail": [
            {
                "loc": ["path", "product_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_successful_delete_single_product(
    test_app_with_db: TestClient, test_product_one: ProductCreate
) -> None:
    post_response = test_app_with_db.post("/api/product", json=test_product_one.dict())

    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    delete_response = test_app_with_db.delete(f"/api/product/{post_content['id']}")

    assert delete_response.status_code == 200

    delete_content = delete_response.json()
    assert delete_content["id"] == post_content["id"]
    assert delete_content["Category"] == test_product_one.Category
    assert delete_content["Variety"] == test_product_one.Variety
    assert delete_content["Packaging"] == test_product_one.Packaging

    get_response = test_app_with_db.get(f"/api/product/{post_content['id']}")
    assert get_response.status_code == 404


def test_unsuccessful_delete_single_product(test_app_with_db: TestClient) -> None:
    delete_response = test_app_with_db.delete(f"/api/product/{None}")
    assert delete_response.status_code == 422
    assert delete_response.json() == {
        "detail": [
            {
                "loc": ["path", "product_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_successful_update_single_product(
    test_app_with_db: TestClient, test_product_one: ProductCreate
) -> None:
    post_response = test_app_with_db.post("/api/product", json=test_product_one.dict())

    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    update_in = ProductUpdate(
        Category="test category UPDATED",
    )

    update_response = test_app_with_db.put(
        f"/api/product/{post_content['id']}", json=update_in.dict(exclude_unset=True)
    )

    assert update_response.status_code == 201

    update_content = update_response.json()
    assert update_content["id"] == post_content["id"]
    assert update_content["Category"] == "test category UPDATED"
    assert update_content["Variety"] == test_product_one.Variety
    assert update_content["Packaging"] == test_product_one.Packaging

    get_response = test_app_with_db.get(f"/api/product/{post_content['id']}")
    assert get_response.status_code == 200
    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Category"] == "test category UPDATED"


def test_unsuccessful_update_single_product(test_app_with_db: TestClient) -> None:
    update_in = ProductUpdate(
        Category="test category UPDATED",
    )

    update_response = test_app_with_db.put(
        f"/api/product/{None}", json=update_in.dict(exclude_unset=True)
    )

    assert update_response.status_code == 422
    assert update_response.json() == {
        "detail": [
            {
                "loc": ["path", "product_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }

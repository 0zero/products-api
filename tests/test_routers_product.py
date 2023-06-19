from fastapi.testclient import TestClient
from tests.helpers import get_random_string

from src.database.schemas.product import ProductCreate, ProductUpdate


def test_successful_post_single_product(test_app_with_db: TestClient) -> None:
    product_in = ProductCreate(
        Category="test category 1",
        Variety=get_random_string(),
        Packaging="test packaging 1",
    )
    response = test_app_with_db.post("/api/product", json=product_in.dict())

    assert response.status_code == 201

    content = response.json()
    assert content["id"] is not None
    assert content["Category"] == product_in.Category
    assert content["Variety"] == product_in.Variety
    assert content["Packaging"] == product_in.Packaging


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


def test_successful_get_single_product(test_app_with_db: TestClient) -> None:
    product_in = ProductCreate(
        Category="test category 1",
        Variety=get_random_string(),
        Packaging="test packaging 1",
    )
    post_response = test_app_with_db.post("/api/product", json=product_in.dict())

    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    get_response = test_app_with_db.get(f"/api/product/{post_content['id']}")

    assert get_response.status_code == 200

    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Category"] == product_in.Category
    assert get_content["Variety"] == product_in.Variety
    assert get_content["Packaging"] == product_in.Packaging


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


def test_successful_get_many_products_with_queries(
    test_app_with_db: TestClient,
) -> None:
    product_in_one = ProductCreate(
        Category="test category 1",
        Variety=get_random_string(),
        Packaging="test packaging 1",
    )
    post_response_one = test_app_with_db.post(
        "/api/product", json=product_in_one.dict()
    )
    assert post_response_one.status_code == 201
    post_content_one = post_response_one.json()
    assert post_content_one["id"] is not None

    product_in_two = ProductCreate(
        Category="test category 1",
        Variety=get_random_string(),
        Packaging="test packaging 1",
    )
    post_response_two = test_app_with_db.post(
        "/api/product", json=product_in_two.dict()
    )
    assert post_response_two.status_code == 201
    post_content_two = post_response_two.json()
    assert post_content_two["id"] is not None

    count_get_response = test_app_with_db.get("/api/product")
    assert count_get_response.status_code == 200
    number_of_products = len(count_get_response.json())

    get_response = test_app_with_db.get(
        f"/api/product?skip={0}&limit={number_of_products}"
    )
    assert get_response.status_code == 200
    get_content = get_response.json()

    assert isinstance(get_content, list)
    assert len(get_content) == number_of_products


def test_successful_delete_single_product(test_app_with_db: TestClient) -> None:
    product_in = ProductCreate(
        Category="test category 1",
        Variety=get_random_string(),
        Packaging="test packaging 1",
    )
    post_response = test_app_with_db.post("/api/product", json=product_in.dict())

    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    delete_response = test_app_with_db.delete(f"/api/product/{post_content['id']}")

    assert delete_response.status_code == 200

    delete_content = delete_response.json()
    assert delete_content["id"] == post_content["id"]
    assert delete_content["Category"] == product_in.Category
    assert delete_content["Variety"] == product_in.Variety
    assert delete_content["Packaging"] == product_in.Packaging

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


def test_successful_update_single_product(test_app_with_db: TestClient) -> None:
    product_in = ProductCreate(
        Category="test category 1",
        Variety=get_random_string(),
        Packaging="test packaging 1",
    )
    post_response = test_app_with_db.post("/api/product", json=product_in.dict())

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
    assert update_content["Variety"] == product_in.Variety
    assert update_content["Packaging"] == product_in.Packaging

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

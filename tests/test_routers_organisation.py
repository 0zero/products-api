from fastapi.testclient import TestClient
from tests.helpers import get_random_string

from src.database.models.base import OrganisationTypeEnum
from src.database.schemas.organisation import OrganisationCreate, OrganisationUpdate


def test_successful_post_single_organisation(test_app_with_db: TestClient) -> None:
    organisation_in = OrganisationCreate(
        Name=get_random_string(),
        Type=OrganisationTypeEnum.BUYER,
    )
    response = test_app_with_db.post("/api/organisation", json=organisation_in.dict())

    assert response.status_code == 201

    content = response.json()
    assert content["id"] is not None
    assert content["Name"] == organisation_in.Name
    assert content["Type"] == organisation_in.Type


def test_failure_to_post_single_organisation(test_app_with_db: TestClient) -> None:
    response = test_app_with_db.post("/api/organisation", json=dict())

    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "Name"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_successful_get_single_organisation(test_app_with_db: TestClient) -> None:
    organisation_in = OrganisationCreate(
        Name=get_random_string(),
        Type=OrganisationTypeEnum.BUYER,
    )

    post_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    get_response = test_app_with_db.get(f"/api/organisation/{post_content['id']}")

    assert get_response.status_code == 200

    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Name"] == organisation_in.Name
    assert get_content["Type"] == organisation_in.Type


def test_unsuccessful_get_single_organisation(test_app_with_db: TestClient) -> None:
    get_response = test_app_with_db.get(f"/api/organisation/{5.4}")
    assert get_response.status_code == 422
    assert get_response.json() == {
        "detail": [
            {
                "loc": ["path", "organisation_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_successful_delete_single_organisation(test_app_with_db: TestClient) -> None:
    organisation_in = OrganisationCreate(
        Name=get_random_string(),
        Type=OrganisationTypeEnum.BUYER,
    )

    post_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    delete_response = test_app_with_db.delete(f"/api/organisation/{post_content['id']}")

    assert delete_response.status_code == 200
    delete_content = delete_response.json()
    assert delete_content["id"] == post_content["id"]
    assert delete_content["Name"] == organisation_in.Name
    assert delete_content["Type"] == organisation_in.Type

    get_response = test_app_with_db.get(f"/api/organisation/{post_content['id']}")

    assert get_response.status_code == 404


def test_unsuccessful_delete_single_organisation(test_app_with_db: TestClient) -> None:
    delete_response = test_app_with_db.delete(f"/api/organisation/{5.4}")
    assert delete_response.status_code == 422
    assert delete_response.json() == {
        "detail": [
            {
                "loc": ["path", "organisation_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_successful_update_single_organisation(test_app_with_db: TestClient) -> None:
    organisation_in = OrganisationCreate(
        Name=get_random_string(),
        Type=OrganisationTypeEnum.BUYER,
    )

    post_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    organisation_update = OrganisationUpdate(
        Type=OrganisationTypeEnum.SELLER,
    )

    put_response = test_app_with_db.put(
        f"/api/organisation/{post_content['id']}",
        json=organisation_update.dict(exclude_unset=True),
    )

    assert put_response.status_code == 201
    put_content = put_response.json()
    assert put_content["id"] == post_content["id"]
    assert put_content["Name"] == organisation_in.Name
    assert put_content["Type"] == organisation_update.Type

    get_response = test_app_with_db.get(f"/api/organisation/{post_content['id']}")
    assert get_response.status_code == 200
    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Name"] == organisation_in.Name
    assert get_content["Type"] == organisation_update.Type


def test_unsuccessful_update_single_organisation(test_app_with_db: TestClient) -> None:
    organisation_in = OrganisationCreate(
        Name=get_random_string(),
        Type=OrganisationTypeEnum.BUYER,
    )

    post_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    organisation_update = OrganisationUpdate(
        Type=OrganisationTypeEnum.SELLER,
    )

    put_response = test_app_with_db.put(
        f"/api/organisation/{None}", json=organisation_update.dict(exclude_unset=True)
    )

    assert put_response.status_code == 422
    assert put_response.json() == {
        "detail": [
            {
                "loc": ["path", "organisation_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


def test_no_change_with_empty_update(test_app_with_db: TestClient) -> None:
    organisation_in = OrganisationCreate(
        Name=get_random_string(),
        Type=OrganisationTypeEnum.BUYER,
    )

    post_response = test_app_with_db.post(
        "/api/organisation", json=organisation_in.dict()
    )
    assert post_response.status_code == 201
    post_content = post_response.json()
    assert post_content["id"] is not None

    organisation_update = OrganisationUpdate()

    put_response = test_app_with_db.put(
        f"/api/organisation/{post_content['id']}",
        json=organisation_update.dict(exclude_unset=True),
    )

    assert put_response.status_code == 201
    put_content = put_response.json()
    assert put_content["id"] == post_content["id"]
    assert put_content["Name"] == organisation_in.Name
    assert put_content["Type"] == organisation_in.Type

    get_response = test_app_with_db.get(f"/api/organisation/{post_content['id']}")
    assert get_response.status_code == 200
    get_content = get_response.json()
    assert get_content["id"] == post_content["id"]
    assert get_content["Name"] == organisation_in.Name
    assert get_content["Type"] == organisation_in.Type

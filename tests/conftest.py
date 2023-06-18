import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.config import Settings, get_settings
from src.main import get_app
from src.database.session import SessionLocal, Session


def get_settings_override():
    """
    Using test database setup here
    """
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app() -> Generator[TestClient, TestClient, None]:
    """
    Generator for a test application to be used in tests. No database added here.
    """
    app = get_app()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def test_db() -> Generator[Session, Session, None]:
    """
    Generator for a test DB to be used in tests.
    """
    yield SessionLocal()

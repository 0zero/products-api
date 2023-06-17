import os
from typing import Generator
import pytest
from starlette.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import Settings, get_settings
from src.main import get_app
from src.database.model import Base
from src.database.session import get_db

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

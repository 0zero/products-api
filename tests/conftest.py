import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import Settings, get_settings
from src.database.models.base import Base
from src.database.session import get_db
from src.main import get_app


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
    test_settings = get_settings_override()
    test_engine = create_engine(test_settings.database_url)
    test_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    connection = test_engine.connect()
    transaction = connection.begin()
    test_session = test_session_local(bind=connection)
    Base.metadata.create_all(bind=test_engine)
    yield test_session
    test_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def test_app_with_db(test_db: Session) -> Generator[TestClient, TestClient, None]:
    """
    Generator for a test application with database.
    """
    app = get_app()
    app.dependency_overrides[get_settings] = get_settings_override

    # Test dependency injection
    def _get_test_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as test_client:
        yield test_client

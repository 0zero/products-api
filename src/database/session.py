from logging import INFO, basicConfig, getLogger
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import get_settings

logger = getLogger(__name__)
basicConfig(level=INFO)

settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.database_url  # type: ignore

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Session, None]:
    """
    Generator for a database session to be used in routers.

    Return: Database session generator
    """

    try:
        logger.info("Initialising database session...")
        db = SessionLocal()
        yield db
    finally:
        logger.info("Closing database session...")
        db.close()

"""Shared pytest fixtures for the Task Management API tests."""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Use a separate test database so we never touch the developer's working database.
os.environ["DATABASE_URL"] = "postgresql+psycopg2://tasks:tasks@localhost:5432/tasks_test"

from app.database import Base, get_db  # noqa: E402  (must come after env var)
from app.main import app  # noqa: E402

engine = create_engine(os.environ["DATABASE_URL"], future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture(scope="session", autouse=True)
def _create_test_database() -> None:
    """Create the tasks_test database if it does not exist, then build tables."""
    admin_engine = create_engine(
        "postgresql+psycopg2://tasks:tasks@localhost:5432/postgres",
        isolation_level="AUTOCOMMIT",
    )
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'tasks_test'")
        ).scalar()
        if not exists:
            conn.execute(text("CREATE DATABASE tasks_test"))
    admin_engine.dispose()

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """Provide a clean database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session) -> TestClient:
    """Provide a TestClient whose requests use the test database session."""

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

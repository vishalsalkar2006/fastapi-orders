# tests/conftest.py
import pytest
from app.core.database import TestingSessionLocal, Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: drop tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


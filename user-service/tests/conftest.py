import pytest

from fastapi.testclient import TestClient

from app.db.base import Base
from app.dependencies.database import get_db
from app.main import app

from tests.test_database import (
    engine,
    TestingSessionLocal
)


Base.metadata.create_all(bind=engine)

def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db
    
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)
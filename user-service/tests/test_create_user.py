from fastapi.testclient import TestClient

from app.main import app


def test_create_user(client):

    payload = {
        "email": "pytest@example.com",
        "first_name": "Py",
        "last_name": "Test",
        "phone": "9999999999"
    }

    response = client.post(
        "/users",
        json=payload
    )

    assert response.status_code == 201
def test_get_user(client):

    payload = {
        "email": "getuser@example.com",
        "first_name": "Get",
        "last_name": "User",
        "phone": "8888888888"
    }

    create_response = client.post(
        "/users",
        json=payload
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.get(
        f"/users/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]


def test_get_invalid_user(client):

    response = client.get("/users/99999")

    assert response.status_code == 404

    assert response.json()["detail"] == "User not found."
def test_delete_user(client):

    payload = {
        "email": "delete@example.com",
        "first_name": "Delete",
        "last_name": "User",
        "phone": "7777777777"
    }

    create_response = client.post(
        "/users",
        json=payload
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.delete(
        f"/users/{user_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/users/{user_id}"
    )

    assert get_response.status_code == 404

    assert get_response.json()["detail"] == "User not found."


def test_delete_invalid_user(client):

    response = client.delete("/users/99999")

    assert response.status_code == 404

    assert response.json()["detail"] == "User not found."
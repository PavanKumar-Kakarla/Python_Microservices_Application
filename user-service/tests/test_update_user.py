def test_update_user(client):

    payload = {
        "email": "update@example.com",
        "first_name": "Old",
        "last_name": "Name",
        "phone": "1111111111"
    }

    create_response = client.post(
        "/users",
        json=payload
    )

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    update_payload = {
        "first_name": "New",
        "phone": "9999999999"
    }

    response = client.put(
        f"/users/{user_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["first_name"] == "New"
    assert data["phone"] == "9999999999"

    assert data["last_name"] == "Name"
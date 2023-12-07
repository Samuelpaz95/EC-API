from test.e2e import client

user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "username": "johndoe",
    "password": "johndoe123",
    "phone_number": "1234567890",
    "address": "123 Main St"
}


def test_post_users():
    print('executing test_post_users')
    response = client.post(
        "v1/users",
        json=user_data
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == user_data["first_name"]
    assert response.json()["last_name"] == user_data["last_name"]
    assert response.json()["username"] == user_data["username"]
    assert response.json()["phone_number"] == user_data["phone_number"]
    assert response.json()["address"] == user_data["address"]
    assert response.json()["id"] == 1
    assert "password" not in response.json()


def test_get_users():
    response = client.get("v1/users")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_user():
    response = client.get("v1/users/1")
    assert response.status_code == 200
    assert response.json()["first_name"] == user_data["first_name"]
    assert response.json()["last_name"] == user_data["last_name"]
    assert response.json()["username"] == user_data["username"]
    assert response.json()["phone_number"] == user_data["phone_number"]
    assert response.json()["address"] == user_data["address"]
    assert response.json()["id"] == 1
    assert "password" not in response.json()


def test_patch_user():
    user_id = 1
    new_data = {
        "first_name": "Jane",
        "username": "janedoe",
        "phone_number": "0987654321",
    }
    response = client.patch(
        f"v1/users/{user_id}",
        json=new_data
    )

    assert response.status_code == 200
    assert response.json()["first_name"] == new_data["first_name"]
    assert response.json()["username"] == new_data["username"]
    assert response.json()["phone_number"] == new_data["phone_number"]
    assert response.json()["id"] == user_id
    assert "password" not in response.json()


def test_delete_user():
    user_id = 1
    response = client.delete(
        f"v1/users/{user_id}",
    )
    assert response.status_code == 200
    response = client.get(
        f"v1/users/{user_id}",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

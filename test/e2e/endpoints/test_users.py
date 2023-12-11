from test.e2e import client, user_data

token = None


def test_post_users():
    response = client.post(
        "v1/auth/sign_up",
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


def test_sign_in():
    response = client.post(
        "v1/auth/sign_in",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"]
    assert "token_type" in response.json()
    global token
    token = response.json()["access_token"]


def test_get_users():
    response = client.get("v1/users/list")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_user():
    response = client.get(
        "v1/users/1", headers={"Authorization": f"Bearer {token}"})
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
        json=new_data,
        headers={"Authorization": f"Bearer {token}"}
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
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    response = client.get(
        f"v1/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

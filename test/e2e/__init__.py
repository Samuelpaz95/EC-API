from re import A
from test.config.database import override_get_db

from fastapi.testclient import TestClient
from pydantic import EmailStr

from main import app
from src.config.database import get_db
from src.modules.authentication.auth_service import AuthService
from src.modules.users.users_schema import User

client = TestClient(app)

user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "username": "johndoe",
    "password": "johndoe123",
    "phone_number": "1234567890",
    "address": "123 Main St"
}


def override_auth_service() -> User:
    data = user_data.copy()
    email = data["email"]
    del data["email"]
    return User(
        id=print('>>>>> HOLA') or 1,
        email=EmailStr(email),
        **data,
    )


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[AuthService()] = override_auth_service

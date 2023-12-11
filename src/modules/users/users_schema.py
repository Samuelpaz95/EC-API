from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.utils import AllOptional


class BaseUser(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=5, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = Field(None, min_length=5, max_length=100)

    class Config:
        schema_extra = dict(example=dict(
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            username="johndoe",
            phone_number="1234567890",
            address="123 Main St"
        ))


class CreateUser(BaseUser):
    password: str = Field(..., min_length=8, max_length=255)

    class Config:
        schema_extra = dict(
            example=dict(**BaseUser.Config.schema_extra.get('example', {}),
                         password="johndoe123"))


class PartialUser(CreateUser, metaclass=AllOptional):

    class Config:
        schema_extra = dict(example=dict(
            first_name="Jane",
            username="janedoe",
            phone_number="0987654321",
        ))


class User(BaseUser):
    id: int = Field(..., gt=0)

    class Config:
        orm_mode = True

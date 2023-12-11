from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=255)

    class Config:
        schema_extra = dict(example=dict(
            email="john.doe@email.com",
            password="johndoe123"
        ))


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        schema_extra = dict(
            example=dict(
                access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJob2F5b3V0dWJlQGdtYWlsLmNvbSIsImV4cCI6MTYyMjg3NjYwNn0.8qX0gJzZ0qDj9YrQ8f7Lw1q7Q6JYfZcUzgJ9Q6Q3y8M",
                token_type="bearer"))

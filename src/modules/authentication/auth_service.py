

import os
from datetime import datetime, timedelta
from http.client import BAD_REQUEST, NOT_FOUND, UNAUTHORIZED
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode

from src.modules.users.users_model import UserDB
from src.modules.users.users_schema import CreateUser, User
from src.modules.users.users_service import UsersService

from .auth_schema import UserLogin

TOKEN_URL = "v1/auth/sign_in"


class AuthService:

    def __init__(self, users_service: UsersService = Depends()) -> None:
        self.users_service = users_service

    def sign_in(self, data: UserLogin):
        user = self.users_service.get_user_by_email(data.email)
        if not user.verify_password(data.password):
            raise HTTPException(NOT_FOUND, detail="User not found")
        return self.create_token(user)

    def sign_up(self, data: CreateUser) -> User:
        try:
            return self.users_service.create_user(data)
        except Exception as e:
            raise HTTPException(BAD_REQUEST, detail=str(e))

    def create_token(self, user: UserDB):
        expiration = timedelta(
            minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", 30)))
        data = dict(sub=user.email,
                    exp=datetime.utcnow() + expiration)
        token = encode(data, os.getenv("JWT_SECRET"),
                       algorithm=os.getenv("ALGORITHM"))
        return token

    def get_current_user(self, token: str):
        credentials_exception = HTTPException(
            UNAUTHORIZED, detail="Could not validate credentials")
        try:
            payload = decode(token, os.getenv("JWT_SECRET"),
                             algorithms=[os.getenv("ALGORITHM", "HS256")])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except PyJWTError:
            raise credentials_exception

        user = self.users_service.get_user_by_email(email)
        if user is None:
            raise credentials_exception
        return user

    def __call__(self, token: Annotated[str, Depends(OAuth2PasswordBearer(
            TOKEN_URL))], user_service: Annotated[UsersService, Depends()]) -> UserDB:
        self.users_service = user_service
        return self.get_current_user(token)

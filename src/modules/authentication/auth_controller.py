from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_restful.cbv import cbv

from src.modules.users.users_schema import CreateUser, User

from .auth_schema import AccessToken, UserLogin
from .auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@cbv(router)
class AuthController:
    def __init__(self, auth_service: AuthService = Depends()) -> None:
        self.auth_service = auth_service

    @router.post("/sign_in", status_code=200)
    async def sign_in(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> AccessToken:
        token = self.auth_service.sign_in(
            UserLogin.construct(
                email=form_data.username,
                password=form_data.password))
        return AccessToken(access_token=token)

    @router.post("/sign_up", status_code=201)
    async def sign_up(self, user_data: CreateUser) -> User:
        return self.auth_service.sign_up(user_data)

    @router.get('/me', status_code=200)
    async def me(self, user: Annotated[User, Depends(AuthService())]) -> User:
        return user

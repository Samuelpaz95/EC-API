from email.headerregistry import ContentDispositionHeader
from typing import Annotated, Dict, List, Literal

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from src.modules.authentication.auth_service import AuthService
from src.utils.types import Paginated

from .users_schema import CreateUser, PartialUser, User
from .users_service import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@cbv(router)
class UserController:

    def __init__(self, users_service: UsersService = Depends()) -> None:
        self.users_service = users_service

    @router.get("/", status_code=200)
    async def get_users_pag(self, page: int = 0, limit: int = 100) -> Paginated[User]:
        response = self.users_service.get_users_pag(page, limit)
        return Paginated[User].from_orm(response)

    @router.get("/list", status_code=200)
    async def get_users(self) -> List[User]:
        users = self.users_service.get_users()
        return [User.from_orm(user) for user in users]

    @router.get("/{user_id}", status_code=200,
                dependencies=[Depends(AuthService())])
    async def get_user(self, user_id: int) -> User:
        return User.from_orm(self.users_service.get_user(user_id))

    @router.post("/", status_code=201, dependencies=[Depends(AuthService())])
    async def create_user(self, user_data: CreateUser) -> User:
        new_user = self.users_service.create_user(user_data)
        return new_user

    @router.patch("/{user_id}", status_code=200,
                  dependencies=[Depends(AuthService())])
    async def update_user(self, user_id: int, partial_user: PartialUser) -> User:
        return User.from_orm(
            self.users_service.update_user(
                user_id, partial_user))

    @router.delete("/{user_id}", status_code=200,
                   dependencies=[Depends(AuthService())])
    async def delete_user(self, user_id: int) -> User:
        return User.from_orm(self.users_service.delete_user(user_id))

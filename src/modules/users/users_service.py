from typing import List

from fastapi import Depends, HTTPException

from src.modules.users.users_model import UserDB

from .users_repository import UsersRepository
from .users_schema import CreateUser, PartialUser, User


class UsersService:
    def __init__(self, users_repository: UsersRepository = Depends()):
        self.users_repository = users_repository

    def get_user(self, user_id) -> UserDB:
        user = self.users_repository.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_users(self) -> List[UserDB]:
        return self.users_repository.get_users()

    def get_users_pag(self, skip: int = 0, limit: int = 100):
        return self.users_repository.get_paginated_users(skip, limit)

    def create_user(self, user: CreateUser):
        new_user = self.users_repository.create_user(user)
        return User.from_orm(new_user)

    def update_user(self, user_id, partial_user: PartialUser) -> UserDB:
        user = self.get_user(user_id)
        return self.users_repository.update_user(user, partial_user)

    def delete_user(self, user_id) -> UserDB:
        user = self.get_user(user_id)
        return self.users_repository.delete_user(user)

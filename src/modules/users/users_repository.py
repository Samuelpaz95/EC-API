from typing import List, Optional

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.utils.types import Paginated

from .users_model import UserDB
from .users_schema import CreateUser, PartialUser


class UsersRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find_user(self, filters: PartialUser) -> Optional[UserDB]:
        query = self.db.query(UserDB)
        query = query.filter_by(**filters.dict(exclude_unset=True))
        return query.first()

    def get_user(self, user_id: int) -> Optional[UserDB]:
        return self.db.query(UserDB).where(UserDB.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[UserDB]:
        return self.db.query(UserDB).filter(UserDB.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserDB]:
        return self.db.query(UserDB).offset(skip).limit(limit).all()

    def get_paginated_users(
            self,
            skip: int = 0,
            limit: int = 100) -> Paginated[UserDB]:
        users = self.db.query(UserDB).offset(skip).limit(limit).all()
        count = self.db.query(UserDB).count()
        has_next = skip + limit < count
        return Paginated[UserDB](
            data=users[:limit],
            total=count,
            page=skip + 1,
            limit=limit,
            has_next=has_next,
            has_prev=skip > 0,
            pages=count // limit
        )

    def create_user(self, user: CreateUser) -> UserDB:
        db_user = UserDB(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user: UserDB, partial_user: PartialUser) -> UserDB:
        user_data = jsonable_encoder(user)
        update_data = partial_user.dict(exclude_unset=True)
        for field in user_data:
            if field in update_data:
                setattr(user, field, update_data[field])
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: UserDB) -> UserDB:
        self.db.delete(user)
        self.db.commit()
        return user

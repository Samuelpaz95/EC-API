from fastapi import APIRouter

from .users import users_router


api_router = APIRouter(prefix="/v1")
api_router.include_router(users_router)


__all__ = ["api_router"]

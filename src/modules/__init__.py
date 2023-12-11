from fastapi import APIRouter

from .users import *
from .authentication import *


api_router = APIRouter(prefix="/v1")
api_router.include_router(users_router)
api_router.include_router(auth_router)


__all__ = ["api_router"]

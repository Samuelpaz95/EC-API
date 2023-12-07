from typing import Generic, List, TypeVar

from pydantic.generics import GenericModel

_T = TypeVar("_T")


class Paginated(GenericModel, Generic[_T]):
    """Paginated Response Model
    """
    data: List[_T]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool
    pages: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

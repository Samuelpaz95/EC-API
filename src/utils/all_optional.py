from typing import Optional

from pydantic import BaseModel
from pydantic.main import ModelMetaclass


class AllOptional(ModelMetaclass):
    def __new__(cls, name, bases, namespaces, **kwargs):

        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
            while hasattr(base, '__base__') and base.__base__ not in [BaseModel, object, None]:
                base = base.__base__
                annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)

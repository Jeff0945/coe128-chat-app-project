from socket import socket
from typing import List, TypeVar, Type


class Collection:
    _T = TypeVar('_T', bound='Collection')
    _items: List[_T] = []

    @classmethod
    def all(cls: Type[_T]) -> List[_T]:
        return cls._items

    @classmethod
    def get(cls: Type[_T], _id: int) -> Type[_T]:
        return next((user for user in cls._items if user.id == _id), None)

    @classmethod
    def create(cls: Type[_T], name: str, connection: socket):
        from models.user import User
        cls._items.append(User(name, connection))

    @classmethod
    def remove(cls: Type[_T], _id: int):
        cls._items.remove(cls.find(_id))

    @classmethod
    def assign_id(cls: Type[_T]):
        return cls._items[-1].id + 1 if len(cls._items) > 0 else 1

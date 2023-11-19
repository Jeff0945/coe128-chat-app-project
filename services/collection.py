from socket import socket
from typing import List, TypeVar, Type


class Collection:
    _T = TypeVar('_T', bound='Collection')
    _items: List[_T] = []
    _filtered: List[_T] = []
    _where_used: bool = False
    required = []

    @classmethod
    def validate(cls, data):
        """
        Ensures that the required keys are present in the provided data before creating instances.

        :param data: Dictionary containing data to validate.
        :raises ValueError: If any required keys are missing in the data.
        """
        if not all(key in data for key in cls.required):
            missing = ', '.join(key for key in cls.required if key not in data)
            raise ValueError(f"Missing: {missing}")

    @classmethod
    def all(cls: Type[_T]) -> List[_T]:
        """
        Retrieves all instances of a subclass.

        :returns List[_T]: List of all instances of the subclass.
        """
        return [item for item in cls._items if isinstance(item, cls)]

    #
    @classmethod
    def get(cls: Type[_T]) -> List[_T]:
        """
        Retrieves either the filtered instances or all instances.

        :returns List[_T]: List of filtered instances or all instances, depending on whether 'where()' has been used.
        """
        data = cls._filtered if cls._where_used else cls.all()
        cls._where_used = False

        return data

    @classmethod
    def find(cls: Type[_T], _id: int) -> Type[_T] | None:
        """
        Locates a specific instance of a subclass by ID.

        :param _id: ID of the instance to find.
        :returns Type[_T] | None: Instance with the given ID or None if not found.
        """
        return next((item for item in cls.all() if item.id == _id and isinstance(item, cls)), None)

    @classmethod
    def create(cls: Type[_T], data: object):
        """
        Adds new instances to the collection.

        :param data: Data to create the new instance.
        """
        cls._items.append(cls(data))

    @classmethod
    def remove(cls: Type[_T], _id: int):
        """
        Removes an instance of a subclass by ID.

        :param _id: ID of the instance to remove.
        """
        to_remove = cls.find(_id)

        if to_remove is not None:
            cls._items.remove(cls.find(_id))

    @classmethod
    def assign_id(cls: Type[_T]):
        """
        Generates a unique ID for a new instance based on existing ones.

        :returns int: Unique ID for a new instance.
        """
        return cls.all()[-1].id + 1 if len(cls.all()) > 0 else 1

    @classmethod
    def where(cls: Type[_T], column: str, condition: str, value) -> Type[_T]:
        """
        Filters instances based on conditions and allows for chaining to refine filters.

        :param column: Name of the attribute to filter on.
        :param condition: Filtering condition (e.g., '=', '>', '<', '!=').
        :param value: Value to compare against.
        :return Type[_T]: Filtered collection of instances based on the conditions.
        """
        cls._where_used = True

        if not cls._filtered:
            cls._filtered = cls.all().copy()

        if condition == "=":
            cls._filtered = [item for item in cls._filtered if getattr(item, column) == value]
        elif condition == ">":
            cls._filtered = [item for item in cls._filtered if getattr(item, column) > value]
        elif condition == "<":
            cls._filtered = [item for item in cls._filtered if getattr(item, column) < value]
        elif condition == "!=":
            cls._filtered = [item for item in cls._filtered if getattr(item, column) != value]
        else:
            raise ValueError("Invalid condition")

        return cls

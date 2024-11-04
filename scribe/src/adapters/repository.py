from abc import ABC
from typing import get_args, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session


class AbstractRepository[T](ABC):

    def add(self, item: T) -> T:
        raise NotImplementedError

    def read(self, id_: int) -> T:
        raise NotImplementedError

    def read_all(
            self,
            offset: int | None = None,
            limit: int | None = None,
            **kwargs
    ) -> Sequence[T]:
        """
        Reads all values from the database for the provided type T.

        :param offset: Optional offset value for pagination implementation.
        :param limit: Optional limit value for pagination implementation.
        :param kwargs: Optional filtering criteria, e.g., field_name=value pairs.
        """
        raise NotImplementedError

    def update(
            self,
            id_: int,
            **kwargs
    ) -> T:
        """
        Updates an existing record in the database identified by the given id.

        :param id_: The unique identifier of the record to be updated.
        :param kwargs: Optional keyword arguments representing the fields to be updated and their new values.
        """
        raise NotImplementedError

    def delete(self, id_: int) -> None:
        raise NotImplementedError


class ItemNotFoundError(LookupError):
    def __init__(self, id_: int):
        super().__init__(f"Item with the id '{id_}' was not found.")


class SqlAlchemyRepository[T](AbstractRepository):

    def __init__(
            self,
            session: Session
    ):
        self.session = session

    def add(self, item: T) -> T:
        self.session.add(item)
        self.session.flush()

        return item

    def read(self, id_: int) -> T:
        """
        :raises ItemNotFoundError: if a nonexistent **id_** is provided.
        """
        type_T = get_args(self.__orig_class__)[0]  # this is the only way to access original type with typing
        statement = select(type_T).where(type_T.id == id_)

        res = self.session.execute(statement).scalar()
        if res is None:
            raise ItemNotFoundError(id_)

        return res

    def read_all(
            self,
            offset: int | None = None,
            limit: int | None = None,
            **kwargs
    ) -> Sequence[T]:
        type_T = get_args(self.__orig_class__)[0]
        statement = select(type_T).offset(offset).limit(limit).filter_by(**kwargs)
        return self.session.execute(statement).scalars().all()

    def update(self, id_: int, **kwargs) -> T:
        """
        :raises ItemNotFoundError: if a nonexistent **id_** is provided.
        """
        type_T = get_args(self.__orig_class__)[0]

        item = self.session.get(type_T, id_)
        if item is None:
            raise ItemNotFoundError(id_)

        item_dict = item.__dict__

        # resolving attributes to be updated in obj_ based on the provided **kwargs
        for key, value in kwargs.items():
            if item_dict.get(key) is not None and value is not None:
                setattr(item, key, value)

        self.session.flush()

        return item

    def delete(self, id_: int) -> None:
        """
        :raises ItemNotFoundError: if a nonexistent **id_** is provided.
        """
        type_T = get_args(self.__orig_class__)[0]

        item = self.session.get(type_T, id_)
        if item is None:
            raise ItemNotFoundError(id_)

        self.session.delete(item)

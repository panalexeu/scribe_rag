from abc import ABC
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session


class AbstractRepository[T](ABC):

    def add(self, item: T) -> None:
        raise NotImplementedError

    def read(self, id_: int) -> T:
        raise NotImplementedError

    def read_all(
            self,
            offset: int | None,
            limit: int | None,
            **kwargs
    ) -> list[T]:
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
    ) -> None:
        """
        Updates an existing record in the database identified by the given id.

        :param id_: The unique identifier of the record to be updated.
        :param kwargs: Optional keyword arguments representing the fields to be updated and their new values.
        """
        raise NotImplementedError

    def delete(self, id_: int) -> None:
        raise NotImplementedError


class SqlAlchemyRepository[T](AbstractRepository):

    def __init__(
            self,
            session: Session,
            type_T: Type[T]
    ):
        self.session = session
        self.type_T = type_T

    def add(self, item: T) -> None:
        self.session.add(item)

    def read(self, id_: int) -> T:
        statement = select(self.type_T).where(self.type_T.id == id_)
        return self.session.execute(statement).scalar()

    def read_all(self, offset: int | None, limit: int | None, **kwargs) -> list[T]:
        statement = select(self.type_T).offset(offset).limit(limit).filter_by(**kwargs)
        return self.session.execute(statement).scalars()

    def update(self, id_: int, **kwargs) -> None:
        obj_ = self.session.get(T, id_)
        obj_dict = obj_.__dict__

        # resolving attributes to be updated in obj_ based on the provided **kwargs
        for key, item in kwargs.items():
            if obj_dict.get(key):
                obj_dict[key] = item

    def delete(self, id_: int) -> None:
        obj_ = self.session.get(T, id_)
        self.session.delete(obj_)

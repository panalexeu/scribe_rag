from abc import ABC
from typing import get_args, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session


class AbstractRepository[T](ABC):

    def add(self, item: T) -> None:
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
            session: Session
    ):
        self.session = session

    def add(self, item: T) -> None:
        self.session.add(item)

    def read(self, id_: int) -> T:
        type_T = get_args(self.__orig_class__)[0]  # this is the only way to access original type with typing, this
        # attribute is set after the object initialization, hence it is not accessible in the constructor and only
        # accessible in methods
        statement = select(type_T).where(type_T.id == id_)
        return self.session.execute(statement).scalar()

    def read_all(
            self,
            offset: int | None = None,
            limit: int | None = None,
            **kwargs
    ) -> Sequence[T]:
        type_T = get_args(self.__orig_class__)[0]  # type of generic T
        statement = select(type_T).offset(offset).limit(limit).filter_by(**kwargs)
        return self.session.execute(statement).scalars().all()

    def update(self, id_: int, **kwargs) -> None:
        type_T = get_args(self.__orig_class__)[0]
        obj_ = self.session.get(type_T, id_)
        obj_dict = obj_.__dict__

        # resolving attributes to be updated in obj_ based on the provided **kwargs
        for key, item in kwargs.items():
            if obj_dict.get(key) is not None and item is not None:
                setattr(obj_, key, item)

    def delete(self, id_: int) -> None:
        type_T = get_args(self.__orig_class__)[0]
        obj_ = self.session.get(type_T, id_)
        self.session.delete(obj_)

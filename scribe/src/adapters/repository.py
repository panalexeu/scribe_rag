from abc import ABC
from typing import get_args, Sequence, Optional, Type

import overrides
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload


class AbstractRepository[T](ABC):

    def add(self, item: T) -> T:
        pass

    def read(self, id_: int) -> T:
        pass

    def read_all(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            **kwargs
    ) -> Sequence[T]:
        """
        Reads all values from the database for the provided type T.

        :param offset: Optional offset value for pagination implementation.
        :param limit: Optional limit value for pagination implementation.
        :param kwargs: Optional filtering criteria, e.g., field_name=value pairs.
        """
        pass

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
        pass

    def delete(self, id_: int) -> None:
        pass

    def count(self) -> int | None:
        pass


class ItemNotFoundError(LookupError):
    def __init__(self, id_: int, item: str):
        super().__init__(f"Item: {item} with the id '{id_}' was not found.")


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
            raise ItemNotFoundError(id_, type_T)

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
            raise ItemNotFoundError(id_, type_T)

        item_dict = item.__dict__

        # resolving attributes to be updated in obj_ based on the provided **kwargs
        for key, value in kwargs.items():
            if key in item_dict:
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
            raise ItemNotFoundError(id_, type_T)

        self.session.delete(item)

    def count(self) -> int | None:
        """
        Counts rows in a type_T table.
        """
        type_T = get_args(self.__orig_class__)[0]
        statement = select(func.count()).select_from(type_T)

        return self.session.execute(statement).scalar()


class SqlAlchemyRelationRepository[T](SqlAlchemyRepository):

    @overrides.override
    def add(self, item: T) -> T:
        type_T = get_args(self.__orig_class__)[0]  # this is the only way to access original type with typing
        self.session.add(item)
        self.session.flush()

        statement = select(type_T).where().options(joinedload('*'))

        return self.session.execute(statement).scalar()

    @overrides.override
    def read(self, id_: int) -> T:
        """
        :raises ItemNotFoundError: if a nonexistent **id_** is provided.
        """
        type_T = get_args(self.__orig_class__)[0]
        statement = select(type_T).where(type_T.id == id_).options(joinedload('*'))

        res = self.session.execute(statement).scalar()
        if res is None:
            raise ItemNotFoundError(id_, type_T)

        return res

    @overrides.override
    def read_all(
            self,
            offset: int | None = None,
            limit: int | None = None,
            **kwargs
    ) -> Sequence[T]:
        type_T = get_args(self.__orig_class__)[0]
        statement = select(type_T).offset(offset).limit(limit).filter_by(**kwargs).options(joinedload('*'))
        return self.session.execute(statement).scalars().all()

    @overrides.override
    def update(self, id_: int, **kwargs) -> T:
        """
        :raises ItemNotFoundError: if a nonexistent **id_** is provided.
        """
        type_T = get_args(self.__orig_class__)[0]

        item = self.session.get(type_T, id_)
        if item is None:
            raise ItemNotFoundError(id_, type_T)

        item_dict = item.__dict__

        # resolving attributes to be updated in obj_ based on the provided **kwargs
        for key, value in kwargs.items():
            if key in item_dict:
                setattr(item, key, value)

        self.session.flush()

        statement = select(type_T).where(type_T.id == id_).options(joinedload('*'))

        return self.session.execute(statement).scalar()

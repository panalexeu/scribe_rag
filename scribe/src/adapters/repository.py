from abc import ABC

from sqlalchemy.orm import Session
from sqlalchemy import select


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

    def __init__(self, session: Session):
        self.session = session

    def add(self, item: T) -> None:
        with self.session as session:
            session.add(item)
            session.commit()

    def read(self, id_: int) -> T:
        with self.session as session:
            return session.get(T, id_)

    def read_all(self, offset: int | None, limit: int | None, **kwargs) -> list[T]:
        with self.session as session:
            statement = select(T).offset(offset).limit(limit).filter_by(**kwargs)
            return session.execute(statement).all()

    def update(self, id_: int, **kwargs) -> None:
        with self.session as session:
            obj_ = session.get(T, id_)
            obj_dict = obj_.__dict__

            # resolving attributes to be updated in obj_ based on the provided **kwargs
            for key, item in kwargs.items():
                if obj_dict.get(key):
                    obj_dict[key] = item

            session.commit()

    def delete(self, id_: int) -> None:
        with self.session as session:
            obj_ = session.get(T, id_)
            session.delete(obj_)
            session.commit()

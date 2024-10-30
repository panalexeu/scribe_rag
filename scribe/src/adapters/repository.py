from abc import ABC


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


class SqlAlchemyRepo[T](AbstractRepository):
    def add(self, item: T) -> None:
        pass

    def read(self, id_: int) -> T:
        pass

    def read_all(self, offset: int | None, limit: int | None, **kwargs) -> list[T]:
        pass

    def update(self, id_: int, **kwargs) -> None:
        pass

    def delete(self, id_: int) -> None:
        pass

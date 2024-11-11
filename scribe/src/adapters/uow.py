from abc import ABC
from typing import Type

from sqlalchemy.orm import Session
from chromadb import AsyncHttpClient

from .repository import SqlAlchemyRepository, AbstractRepository


class AbstractUoW(ABC):
    """
    An abstract base class for the Unit of Work pattern, requiring implementers to provide a repository instance for
    managing transactional operations.
    """
    repository: AbstractRepository

    def commit(self):
        pass

    def rollback(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class AsyncAbstractUoW(ABC):
    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass


class SqlAlchemyUoW(AbstractUoW):
    """
    Simple abstraction on top of SQLAlchemy's session UoW. I could use the session's UoW, but this
    would tightly couple my app with the SQLAlchemy. That's why this class is needed.

    Rollbacks in case of exceptions or exit. Commits should be explicit.
    """

    def __init__(
            self,
            repository: Type[SqlAlchemyRepository],
            session: Session
    ):
        self.session = session
        self.repository = repository(self.session)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()

from abc import ABC
from typing import Type

from .repository import SqlAlchemyRepository
from sqlalchemy.orm import Session


class AbstractUoW(ABC):

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, *args):
        raise NotImplementedError


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
        self.rollback()

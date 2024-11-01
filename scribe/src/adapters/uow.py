from abc import ABC

from .repository import SqlAlchemyRepository
from sqlalchemy.orm import Session


class AbstractUoW(ABC):

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class SqlAlchemyUoW(AbstractUoW):

    def __init__(
            self,
            repository: SqlAlchemyRepository,
            session: Session
    ):
        self.repository = repository
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

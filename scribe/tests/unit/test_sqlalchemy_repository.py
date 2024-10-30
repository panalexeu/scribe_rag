import pytest

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from src.adapters.orm_models import map_sqlalchemy_models
from src.di_container import Container
from src.adapters.repository import SqlAlchemyRepository


# @pytest.fixture(scope='function')
# def setup_session():
#     container = Container()
#     engine = create_engine("sqlite:///:memory", echo=True)
#     map_sqlalchemy_models()
#     container.registry().metadata.create_all(engine)
#     session = Session(engine)
#     yield SqlAlchemyRepository()


def test_repo_add_method():
    pass

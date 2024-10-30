"""
Consider this test module as the place to experiment with a sqlalchemy orm related things, encapsulated in tests.
"""
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import clear_mappers

from src.adapters.orm_models import map_sqlalchemy_models
from src.di_container import Container
from src.domain.models import FakeModel


@pytest.fixture(scope='function')
def setup_orm_session():
    container = Container()
    engine = create_engine('sqlite:///:memory:', echo=True)
    map_sqlalchemy_models()
    container.registry().metadata.create_all(engine)
    yield Session(engine)
    clear_mappers()


def test_fake_model_orm_mapping(setup_orm_session):
    with setup_orm_session as session:
        fake1 = FakeModel(
            True,
            'cool-ship'
        )
        fake2 = FakeModel(
            False,
            'infinity'
        )

        session.add_all([fake1, fake2])

        session.get(FakeModel, 1)
        session.get(FakeModel, 2)

        # ApiKeyCredential objects are successfully retrieved from the db
        # with the new mapped field
        assert fake1.id == 1
        assert fake2.id == 2
        assert isinstance(fake1.datetime, datetime)
        assert isinstance(fake2.datetime, datetime)


def test_fake_model_update(setup_orm_session):
    init_name = 'stars-1'
    with setup_orm_session as session:
        fake = FakeModel(
            True,
            init_name
        )

        # adding model and retrieving it
        session.add(fake)
        session.get(FakeModel, 1)

        # the name is the same
        assert fake.spaceship == init_name

        # updating the name updates it in session
        fake.spaceship = 'cosmos-3'
        session.get(FakeModel, 1)

        assert fake.spaceship != init_name

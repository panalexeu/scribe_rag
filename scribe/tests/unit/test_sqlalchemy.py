"""
Consider this test module as the place to experiment with a sqlalchemy orm related things, encapsulated in tests.
"""
from datetime import datetime

import pytest
from faker import Faker
from sqlalchemy.orm import clear_mappers

from src.adapters.orm_models import map_sqlalchemy_models
from src.adapters.uow import SqlAlchemyUoW
from src.adapters.repository import SqlAlchemyRepository
from src.di_container import Container
from src.domain.models import FakeModel


@pytest.fixture(scope='module')
def fake_session():
    container = Container()
    map_sqlalchemy_models(container.registry())
    container.registry().metadata.create_all(container.engine())
    yield container.session()


@pytest.fixture(scope='module')
def faker():
    return Faker()


def test_fake_model_orm_mapping(fake_session):
    with fake_session as session:
        fake1 = FakeModel(
            True,
            'cool-ship'
        )
        fake2 = FakeModel(
            False,
            'infinity'
        )

        session.add_all([fake1, fake2])

        session.flush()

        session.get(FakeModel, 1)
        session.get(FakeModel, 2)

        # FakeModel objects are successfully retrieved from the db
        # with the new mapped fields (id, datetime)
        assert fake1.id == 1
        assert fake2.id == 2
        assert isinstance(fake1.datetime, datetime)
        assert isinstance(fake2.datetime, datetime)


def test_fake_model_update(fake_session):
    init_name = 'stars-1'
    with fake_session as session:
        fake = FakeModel(
            True,
            init_name
        )

        # adding model and retrieving it
        session.add(fake)
        session.flush()
        session.get(FakeModel, 1)

        # the name is the same
        assert fake.spaceship == init_name

        # updating the name updates it in the session
        fake.spaceship = 'cosmos-3'
        session.get(FakeModel, 1)

        assert fake.spaceship != init_name


def test_add_sqlalchemy_repository_method(fake_session):
    with fake_session as session:
        fake1 = FakeModel(
            True,
            'fallen-angel'
        )

        repo = SqlAlchemyRepository[FakeModel](session)
        repo.add(fake1)

        session.flush()
        session.get(FakeModel, 1)

        # model was successfully added since it has autoincremented id attribute
        assert fake1.id == 1


def test_read_sqlalchemy_repository_method(fake_session):
    with fake_session as session:
        fake = FakeModel(
            False,
            'terrifier'
        )
        session.add(fake)
        session.flush()

        repo = SqlAlchemyRepository[FakeModel](session)
        read_fake = repo.read(1)

        # assert that fake and read fake are the same instances with ids
        assert fake.id == 1
        assert read_fake is fake


# TODO add filter by test for read all
def test_read_all_sqlalchemy_repository_method(fake_session):
    with fake_session as session:
        fakes = [
            FakeModel(True, '123'),
            FakeModel(False, 'jhon-11')
        ]

        session.add_all(fakes)
        session.flush()

        repo = SqlAlchemyRepository[FakeModel](session)
        read_fakes = repo.read_all()

        for fake1, fake2 in zip(fakes, read_fakes):
            assert fake1 is fake2


def test_read_all_sqlalchemy_repository_with_limit_and_offset(fake_session, faker):
    with fake_session as session:
        fakes = [FakeModel(True, faker.military_ship()) for _ in range(20)]

        session.add_all(fakes)
        session.flush()

        repo = SqlAlchemyRepository[FakeModel](session)
        page1 = repo.read_all(0, 10)
        page2 = repo.read_all(10, 10)

        # assert that page sizes equals 10
        assert len(page1) == len(page2) == 10

        # assert that the same objects are read
        for fake1, page1 in zip(fakes[:10], page1):
            assert fake1 is page1

        for fake2, page2 in zip(fakes[10:], page2):
            assert fake2 is page2


def test_update_sqlalchemy_repository_method(fake_session, faker):
    with fake_session as session:
        fake = FakeModel(
            False,
            faker.military_ship()
        )

        session.add(fake)
        session.flush()

        # updating the fake object
        repo = SqlAlchemyRepository[FakeModel](session)
        repo.update(1, portal_gun=True, spaceship='alex-11')

        # retrieving it
        session.get(FakeModel, 1)

        # asserting that fake object was updated
        assert fake.spaceship == 'alex-11'
        assert fake.portal_gun is True
        assert fake.id == 1


def test_update_sqlalchemy_repo_does_not_updates_not_existing_attributes(fake_session, faker):
    with fake_session as session:
        fake = FakeModel(
            True,
            faker.military_ship()
        )

        session.add(fake)
        session.flush()

        # updating the fake object with irrelevant 'age' attribute
        repo = SqlAlchemyRepository[FakeModel](session)
        repo.update(1, age=0, spaceship='jhon-11')

        # retrieving it
        session.get(FakeModel, 1)

        # asserting that age does not exist and only spaceship is changed
        assert fake.id == 1
        assert fake.spaceship == 'jhon-11'
        assert fake.portal_gun is True
        with pytest.raises(AttributeError):
            fake.age


def test_update_sqlalchemy_repo_method_does_nothing_when_attributes_are_none(fake_session, faker):
    with fake_session as session:
        fake = FakeModel(
            True,
            faker.military_ship()
        )

        session.add(fake)
        session.flush()

        # updating the fake object with None attributes
        repo = SqlAlchemyRepository[FakeModel](session)
        repo.update(1, spaceship=None, portal_gun=False)

        # retrieving the updated object
        session.get(FakeModel, 1)

        # spaceship is not None, portal gun is changed
        assert fake.id == 1
        assert fake.spaceship is not None
        assert fake.portal_gun == False


def test_delete_sqlalchemy_repo_method(fake_session, faker):
    with fake_session as session:
        fake = FakeModel(
            True,
            faker.military_ship()
        )

        # adding object to the sesssion
        session.add(fake)
        session.flush()
        session.get(FakeModel, 1)

        repo = SqlAlchemyRepository[FakeModel](session)
        repo.delete(1)
        session.flush()  # flushing the changes

        # assert that fake is indeed deleted
        assert session.get(FakeModel, 1) is None


def test_sqlalchemy_uow_exit_rollbacks(fake_session):
    faker = Faker()

    sqlalchemy_uow = SqlAlchemyUoW(
        SqlAlchemyRepository[FakeModel],
        fake_session
    )

    with sqlalchemy_uow as uow:
        # adding a model but not commiting it
        fake = FakeModel(
            True,
            faker.military_ship()
        )
        uow.repository.add(fake)

    with sqlalchemy_uow as uow:
        # the model is not in the session and is not retrieved
        read_fake = uow.repository.read(1)
        assert read_fake is None


def test_sqlalchemy_uow_commit(fake_session):
    sqlalchemy_uow = SqlAlchemyUoW(
        SqlAlchemyRepository[FakeModel],
        fake_session
    )

    with sqlalchemy_uow as uow:
        # adding a model and commiting it
        fake = FakeModel(
            True,
            'alex-11'
        )
        uow.repository.add(fake)
        uow.commit()

    with sqlalchemy_uow as uow:
        # the model is successfully retrieved
        read_fake = uow.repository.read(1)

        assert read_fake is fake
        assert read_fake.id == fake.id == 1

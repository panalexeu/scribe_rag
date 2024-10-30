from copy import copy
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.domain.models import ApiKeyCredential
from src.domain.services import encode_api_key_credential
from src.adapters.codecs import FakeCodec
from src.adapters.orm_models import map_sqlalchemy_models
from src.di_container import Container


@pytest.fixture(scope='module')
def setup_orm_session():
    container = Container()
    engine = create_engine('sqlite:///:memory:', echo=True)
    map_sqlalchemy_models()
    container.registry().metadata.create_all(engine)
    yield Session(engine)


def test_encode_api_key_credential_service():
    api_key_credential = ApiKeyCredential('fake-api', 'fake-key')
    api_key_credential_copy = copy(api_key_credential)
    codec = FakeCodec('fake-key')

    encode_api_key_credential(api_key_credential, codec)

    # only api key is modified by codec encoding
    assert api_key_credential.api_key != api_key_credential_copy.api_key
    assert api_key_credential.name == api_key_credential_copy.name


def test_api_key_orm_mapping(setup_orm_session):
    with setup_orm_session as session:
        open_ai = ApiKeyCredential(
            'open-ai',
            '12345'
        )
        cohere = ApiKeyCredential(
            'cohere',
            '123415'
        )

        session.add_all([open_ai, cohere])

        new_openai: ApiKeyCredential = session.get(ApiKeyCredential, 1)
        new_cohere: ApiKeyCredential = session.get(ApiKeyCredential, 2)

        # ApiKeyCredential objects are successfully retrieved from the db
        assert new_openai.name == open_ai.name
        assert new_cohere.name == cohere.name
        assert new_cohere.api_key == cohere.api_key
        assert new_openai.api_key == open_ai.api_key


def test_api_key_encode_service_and_orm_mapping(setup_orm_session):
    init_api_key = '12345'
    with setup_orm_session as session:
        credential = ApiKeyCredential(
            'fake-cred',
            init_api_key
        )

        # encode api key in the credential object
        encode_api_key_credential(credential, FakeCodec('fake-key'))

        session.add(credential)

        retrieved_cred: ApiKeyCredential = session.get(ApiKeyCredential, 1)

        # assert that key was encoded and not equals init_api_key
        assert retrieved_cred.api_key != init_api_key


def test_datetime_is_mapped_to_api_key_credential(setup_orm_session):
    with setup_orm_session as session:
        credential = ApiKeyCredential(
            'fake-cred',
            'fake-key'
        )

        # adding new entity to the session
        session.add(credential)

        # flushing changes
        session.flush()

        # datetime is mapped to the credential object
        assert isinstance(credential.datetime, datetime)

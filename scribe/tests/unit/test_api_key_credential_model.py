from copy import copy

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from rich import print

from src.domain.models import ApiKeyCredential
from src.domain.services import encode_api_key_credential
from src.adapters.codecs import FernetCodec
from src.adapters.orm_models import map_orm_models
from src.di_container import Container


@pytest.fixture(scope='function')
def setup_orm_session():
    container = Container()
    engine = create_engine('sqlite:///:memory:', echo=True)
    map_orm_models()
    container.registry().metadata.create_all(engine)
    yield Session(engine)


def test_encode_api_key_credential():
    api_key_credential = ApiKeyCredential('fake-api', 'fake-key')
    api_key_credential_copy = copy(api_key_credential)
    codec = FernetCodec(key=Fernet.generate_key())

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
        session.commit()

    with setup_orm_session as session:
        new_openai: ApiKeyCredential = session.get(ApiKeyCredential, 1)
        new_cohere: ApiKeyCredential = session.get(ApiKeyCredential, 2)
        print(new_openai, new_cohere)

        # ApiKeyCredential objects are successfully retrieved from the db
        assert new_openai.name == 'open-ai'
        assert new_cohere.name == 'cohere'
        assert new_cohere.api_key == '123415'
        assert new_openai.api_key == '12345'

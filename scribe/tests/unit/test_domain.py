import json
from copy import copy

import pytest

from src.adapters.codecs import FakeCodec
from src.domain.services import EncodeApiKeyCredentialService
from src.domain.models import (
    ApiKeyCredential,
    DocProcessingConfig,
    ChatModel
)
from src.enums import (
    ChunkingStrategy,
    Postprocessor,
    ChatModelName
)


def test_encode_api_key_credential_service():
    api_key_credential = ApiKeyCredential('fake-api', 'fake-key')
    api_key_credential_copy = copy(api_key_credential)

    # encoding the api key and setting encoding service
    codec = FakeCodec('fake-key')
    encode_service = EncodeApiKeyCredentialService(codec)
    encode_service.encode(api_key_credential)

    # only api key is modified by codec encoding
    assert api_key_credential.api_key != api_key_credential_copy.api_key
    assert api_key_credential.name == api_key_credential_copy.name


def test_doc_proc_cnf_forms_json_config():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
        None,
        None,
        None,
        None
    )

    # json config is successfully formed
    dict_ = json.loads(config.json_config)
    assert isinstance(dict_, dict)
    assert dict_['postprocessors'] == ['clean', 'clean_bullets']
    assert dict_['chunking_strategy'] == 'basic'


def test_doc_proc_cnf_sets_up_chunking_params_as_None_if_no_chunking_strategy_provided():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        None,
        10,
        123,
        12,
        True
    )

    assert config.max_characters is None
    assert config.new_after_n_chars is None
    assert config.overlap is None
    assert config.overlap_all is None


def test_doc_proc_cnf_sets_up_default_values_if_chunking_strategy_provided_but_chunking_params_is_None():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
        None,
        None,
        None,
        None
    )

    assert config.max_characters == config.new_after_n_chars == 500
    assert config.overlap == 0
    assert config.overlap_all is False


@pytest.fixture(scope='function')
def chat_model():
    return ChatModel(
        ChatModelName.GPT_4O,
        1,
        2,
        0.1,
        'web.com',
        1,
        3,
        ['yes', 'no'],
    )


def test_chat_model_returns_json_string(chat_model):
    assert isinstance(chat_model.json_str, str)


def test_chat_model_is_serializable(chat_model):
    dict_ = json.loads(chat_model.json_str)

    # everything is serializable except the model name, api key credential id and json_str
    attr_dict = chat_model.__dict__
    attr_dict.pop('model_name')
    attr_dict.pop('api_key_credential_id')
    attr_dict.pop('json_str')

    # attr_dict and dict_ are the same
    assert attr_dict == dict_


def test_chat_model_is_deserializable(chat_model):
    json_str = chat_model.json_str

    # since model_name and api_key_credential_id are not serializable, we provide them with the json_str
    deserialized_chat_model = ChatModel.deserialize(
        json_str,
        model_name=chat_model.model_name,
        api_key_credential_id=chat_model.api_key_credential_id
    )

    assert isinstance(deserialized_chat_model, ChatModel)
    assert deserialized_chat_model.__dict__ == chat_model.__dict__

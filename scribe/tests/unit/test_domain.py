import json
from copy import copy

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
from src.adapters.codecs import FakeCodec


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


def test_doc_proc_cnf_serializes_postprocessors():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
        None,
        None,
        None,
        None
    )

    assert isinstance(config.postprocessors, str)


def test_doc_proc_cnf_sets_up_chunking_params_as_none_if_no_chunking_strategy_provided():
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


def test_doc_proc_cnf_sets_up_default_values_if_chunking_strategy_provided_but_chunking_params_is_none():
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


def test_chat_model_serializes_stop_sequences_to_json_string():
    chat_model = ChatModel(
        ChatModelName.GPT_4O,
        1,
        2,
        0.1,
        'web.com',
        1,
        3,
        ['yes', 'no'],
    )

    assert isinstance(chat_model.stop_sequences, str)


def test_chat_model_deserializes_stop_sequences_to_list_str():
    seq = ['yes', 'no']
    chat_model = ChatModel(
        ChatModelName.GPT_4O,
        1,
        2,
        0.1,
        'web.com',
        1,
        3,
        seq
    )

    assert isinstance(chat_model.stop_sequences, str)
    assert chat_model.deserialized_stop_sequence == seq


def test_chat_model_doesnt_serialize_and_deserialize_none_stop_sequence():
    chat_model = ChatModel(
        ChatModelName.GPT_4O,
        1,
        2,
        0.1,
        'web.com',
        1,
        3,
        None
    )

    assert chat_model.stop_sequences is None
    assert chat_model.deserialized_stop_sequence is None


# def test_chat_model_builder_builds_models():
#     codec = FakeCodec('fake-key')
#     open_ai = ChatModel(
#         ChatModelName.GPT_4O,
#         1,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#     )
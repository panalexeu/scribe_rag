import json
from copy import copy

from src.adapters.codecs import FakeCodec
from src.domain.services import EncodeApiKeyCredentialService
from src.domain.models import (
    ApiKeyCredential,
    DocProcessingConfig
)
from src.enums import ChunkingStrategy, UnstructuredPostprocessors

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


def test_doc_processing_json_config_forms():
    config = DocProcessingConfig(
        'fake',
        [UnstructuredPostprocessors.CLEAN, UnstructuredPostprocessors.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
    )

    # json is successfully created
    dict_ = json.loads(config.json_config)
    assert isinstance(dict_, dict)
    assert dict_['postprocessors'] == ['clean', 'clean_bullets']
    assert dict_['chunking_strategy'] == 'basic'

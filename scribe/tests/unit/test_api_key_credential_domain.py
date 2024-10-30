from copy import copy

from src.adapters.codecs import FakeCodec
from src.domain.models import ApiKeyCredential
from src.domain.services import encode_api_key_credential


def test_encode_api_key_credential_service():
    api_key_credential = ApiKeyCredential('fake-api', 'fake-key')
    api_key_credential_copy = copy(api_key_credential)
    codec = FakeCodec('fake-key')

    encode_api_key_credential(api_key_credential, codec)

    # only api key is modified by codec encoding
    assert api_key_credential.api_key != api_key_credential_copy.api_key
    assert api_key_credential.name == api_key_credential_copy.name

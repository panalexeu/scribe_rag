import pytest
from cryptography.fernet import Fernet

from src.adapters.codecs import (
    FernetCodec
)


@pytest.fixture(scope='module')
def fernet_key():
    return Fernet.generate_key()


def test_fernet_codec_encodes_and_decodes_data(fernet_key):
    codec = FernetCodec(fernet_key)
    data = 'lorem ipsum'

    encoded_data = codec.encode(data)
    decoded_data = codec.decode(encoded_data)

    assert data == decoded_data

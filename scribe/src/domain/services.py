from .models import ApiKeyCredential
from src.adapters.codecs import AbstractCodec


def encode_api_key_credential(
        api_key_credential: ApiKeyCredential,
        codec: AbstractCodec
) -> None:
    """
    Encodes api key of the provided ApiKeyCredential object,
    using the provided codec.
    """
    api_key_credential.api_key = codec.encode(api_key_credential.api_key)


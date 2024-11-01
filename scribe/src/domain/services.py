from .models import ApiKeyCredential
from src.adapters.codecs import AbstractCodec


class EncodeApiKeyCredentialService:
    """
    Encodes api key of the provided ApiKeyCredential object,
    using the provided codec.
    """

    def __init__(self, codec: AbstractCodec):
        self.codec = codec

    def encode(self, api_key_cred: ApiKeyCredential):
        api_key_cred.api_key = self.codec.encode(api_key_cred.api_key)

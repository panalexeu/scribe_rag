from abc import ABC

from cryptography.fernet import Fernet


class AbstractCodec(ABC):

    def __init__(self, key):
        self.key = key

    def encode(self, data: str) -> str:
        raise NotImplementedError

    def decode(self, encoded_data: str) -> str:
        raise NotImplementedError

    @classmethod
    def gen_key(cls) -> str:
        raise NotImplementedError


class FakeCodec(AbstractCodec):

    def encode(self, data: str) -> str:
        return 'encoded_data'

    def decode(self, encoded_data: str) -> str:
        return 'decoded_data'

    @classmethod
    def gen_key(cls) -> str:
        return 'fake-key'


class FernetCodec(AbstractCodec):
    def encode(self, data: str) -> str:
        byte_content = data.encode()
        byte_encode = Fernet(self.key).encrypt(byte_content)
        str_encode = byte_encode.decode()

        return str_encode

    def decode(self, encoded_data: str) -> str:
        byte_decoded_content = Fernet(self.key).decrypt(encoded_data)
        str_decode = byte_decoded_content.decode()

        return str_decode

    @classmethod
    def gen_key(cls) -> str:
        """
        Provides base64-encoded (base64.urlsafe_b64encode) 32-byte generated key (os.urandom).

        :returns: str - A generated base64-encoded 32-byte key.
        """
        byte_key = Fernet.generate_key()
        str_key = byte_key.decode()

        return str_key

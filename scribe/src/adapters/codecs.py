from abc import ABC

from cryptography.fernet import Fernet


class AbstractCodec(ABC):

    def __init__(self, key):
        self.key = key

    def encode(self, data: str) -> str:
        raise NotImplementedError

    def decode(self, encoded_data: str) -> str:
        raise NotImplementedError


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

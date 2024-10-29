from abc import ABC

from cryptography.fernet import Fernet


class AbstractCodec(ABC):

    def encode(self, content: str, key: str) -> str:
        raise NotImplementedError

    def decode(self, encoded_content: str, key: str) -> str:
        raise NotImplementedError


class FernetCodec(AbstractCodec):
    def encode(self, content: str, key: str) -> str:
        pass

    def decode(self, encoded_content: str, key: str) -> str:
        pass


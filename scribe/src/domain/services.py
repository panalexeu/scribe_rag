import io
from typing import Type

from .models import ApiKeyCredential
from src.adapters.codecs import AbstractCodec

from langchain_core.document_loaders.base import BaseLoader, Document


class EncodeApiKeyCredentialService:
    """
    Encodes api key of the provided ApiKeyCredential object,
    using the provided codec.
    """

    def __init__(self, codec: AbstractCodec):
        self.codec = codec

    def encode(self, api_key_cred: ApiKeyCredential):
        api_key_cred.api_key = self.codec.encode(api_key_cred.api_key)


class LoadDocumentFactoryService:
    """
    Service that wraps around langchain_core.document_loaders.base.BaseLoader
    to load documents asynchronously.
    Works with loaders like:
        - langchain_unstructured.document_loaders.UnstructuredLoader;
    """

    def __init__(self, doc_loader: Type[BaseLoader]):
        self.doc_loader = doc_loader

    # TODO make the loop truly async
    async def load_async(self, files: dict[str, bytes]) -> list[Document]:
        all_docs = []
        for filename, bytes_ in files.items():
            wrapped_bytes = io.BytesIO(bytes_)  # <-- BytesIO wrapping around bytes
            document_loader = self.doc_loader(
                file=wrapped_bytes,  # type: ignore
                metadata_filename=filename  # type: ignore
            )
            docs = await document_loader.aload()
            all_docs.extend(docs)

        return all_docs

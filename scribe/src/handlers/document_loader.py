import io

from typing import Type
from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from langchain_core.documents import Document
from langchain_core.document_loaders.base import BaseLoader
from langchain_unstructured.document_loaders import UnstructuredLoader

from src.di_container import Container


class DocumentLoadCommand(GenericQuery[list[Document]]):
    def __init__(self, files: dict[str, bytes]):
        self.files = files


@Mediator.handler
class DocumentLoadHandler:

    @inject
    def __init__(
            self,
            document_loader: Type[BaseLoader] = Provide[Container.document_loader]
    ):
        self.document_loader = document_loader

    async def handle(self, request: DocumentLoadCommand) -> list[Document]:
        all_docs = []
        for filename, bytes_ in request.files.items():
            wrapped_bytes = io.BytesIO(bytes_)
            document_loader = self.document_loader(
                file=wrapped_bytes,  # type: ignore
                metadata_filename=filename  # type: ignore
            )
            docs = await document_loader.aload()
            all_docs.extend(docs)

        return all_docs

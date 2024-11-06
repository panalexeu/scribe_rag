import io
from typing import Type

from dependency_injector.wiring import inject, Provide
from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from mediatr import Mediator, GenericQuery

from src.domain.services import LoadDocumentService
from src.di_container import Container


class LoadDocumentCommand(GenericQuery[list[Document]]):
    def __init__(self, files: dict[str, bytes]):
        self.files = files


@Mediator.handler
class LoadDocumentHandler:

    @inject
    def __init__(
            self,
            load_doc_service: LoadDocumentService = Provide[Container.load_document_service]
    ):
        self.load_doc_service = load_doc_service

    async def handle(self, request: LoadDocumentCommand) -> list[Document]:
        return await self.load_doc_service.load_async(request.files)

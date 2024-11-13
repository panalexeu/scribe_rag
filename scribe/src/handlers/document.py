from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from pydantic import BaseModel
from rich import print

from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.services.load_document_service import LoadDocumentService


class DocAddModel(BaseModel, GenericQuery[...]):
    vec_col_name: str
    doc_processing_cnf_id: int
    files: dict[str, bytes] | None
    url: str | None


@Mediator.handler
class DocAddHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow],
            load_document_service: LoadDocumentService = Provide[Container.load_document_service]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow
        self.load_document_service = load_document_service

    async def handle(self, request: DocAddModel) -> ...:
        with self.doc_proc_cnf_uow as uow:
            doc_proc_cnf = uow.repository.read(request.doc_processing_cnf_id)

        loaded_docs = await self.load_document_service.load_async(
            files=request.files,
            url=request.url,
            doc_proc_cnf=doc_proc_cnf
        )

        print(loaded_docs)

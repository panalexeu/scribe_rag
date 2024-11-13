from typing import Type

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from pydantic import BaseModel

from src.adapters.async_vector_client import AbstractAsyncClient
from src.adapters.uow import AbstractUoW
from src.adapters.vector_collection_repository import (
    AbstractAsyncVectorCollectionRepository,
    AbstractAsyncDocumentRepository
)
from src.di_container import Container
from src.domain.services.load_document_service import LoadDocumentService
from src.adapters.chroma_models import VectorChromaDocument


class DocAddCommand(BaseModel, GenericQuery[None]):
    vec_col_name: str
    doc_processing_cnf_id: int
    files: dict[str, bytes] | None
    urls: list[str] | None


@Mediator.handler
class DocAddHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow],
            load_document_service: LoadDocumentService = Provide[Container.load_document_service],
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow
        self.load_document_service = load_document_service
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocAddCommand) -> None:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        with self.doc_proc_cnf_uow as uow:
            doc_proc_cnf = uow.repository.read(request.doc_processing_cnf_id)

        loaded_docs = await self.load_document_service.load_async(
            files=request.files,
            urls=request.urls,
            doc_proc_cnf=doc_proc_cnf
        )

        return await async_doc_repo.add(loaded_docs)


class DocReadAllQuery(BaseModel, GenericQuery[list[VectorChromaDocument]]):
    vec_col_name: str
    limit: int | None
    offset: int | None


@Mediator.handler
class DocReadAllHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow],
            load_document_service: LoadDocumentService = Provide[Container.load_document_service],
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow
        self.load_document_service = load_document_service
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocReadAllQuery) -> list[VectorChromaDocument]:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        return await async_doc_repo.read_all(
            limit=request.limit,
            offset=request.offset
        )


class DocCountQuery(BaseModel, GenericQuery[int]):
    vec_col_name: str


@Mediator.handler
class DocCountHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow],
            load_document_service: LoadDocumentService = Provide[Container.load_document_service],
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow
        self.load_document_service = load_document_service
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocCountQuery) -> int:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        return await async_doc_repo.count()


class DocDeleteCommand(BaseModel, GenericQuery[None]):
    vec_col_name: str
    doc_name: str


@Mediator.handler
class DocDeleteHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow],
            load_document_service: LoadDocumentService = Provide[Container.load_document_service],
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow
        self.load_document_service = load_document_service
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocDeleteCommand) -> None:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        return await async_doc_repo.delete(request.doc_name)


class DocPeekQuery(BaseModel, GenericQuery[list[VectorChromaDocument]]):
    vec_col_name: str


@Mediator.handler
class DocPeekHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow],
            load_document_service: LoadDocumentService = Provide[Container.load_document_service],
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow
        self.load_document_service = load_document_service
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocPeekQuery) -> list[VectorChromaDocument]:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        return await async_doc_repo.peek()

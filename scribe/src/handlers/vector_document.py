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
from src.domain.services.embedding_model_builder import EmbeddingModelBuilder
from src.domain.models import VectorCollection


class DocAddCommand(BaseModel, GenericQuery[None]):
    id_: int
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
            domain_vector_collection_uow: AbstractUoW = Provide[Container.domain_vector_collection_uow],
            embedding_model_builder_service: EmbeddingModelBuilder = Provide[Container.embedding_model_builder]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow
        self.load_document_service = load_document_service
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client
        self.domain_vector_collection_uow = domain_vector_collection_uow
        self.embedding_model_builder_service = embedding_model_builder_service

    async def handle(self, request: DocAddCommand) -> None:
        with self.domain_vector_collection_uow as uow:
            # retrieve domain vec col
            vec_col_obj: VectorCollection = uow.repository.read(id_=request.id_)

            # retrieve vec col from vector db
            async_vec_db_client = await self.async_vector_db_client.async_init()
            vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
            ef = self.embedding_model_builder_service.build(vec_col_obj.embedding_model)
            collection = await vector_collection_repo.read(vec_col_obj.name, embedding_function=ef)

        with self.doc_proc_cnf_uow as uow:
            doc_proc_cnf = uow.repository.read(request.doc_processing_cnf_id)

        loaded_docs = await self.load_document_service.load_async(
            files=request.files,
            urls=request.urls,
            doc_proc_cnf=doc_proc_cnf
        )

        async_doc_repo = self.async_document_repository(collection)  # type: ignore
        return await async_doc_repo.add(loaded_docs)


class DocReadAllQuery(BaseModel, GenericQuery[list[VectorChromaDocument]]):
    id_: int
    limit: int | None
    offset: int | None


@Mediator.handler
class DocReadAllHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
            domain_vector_collection_uow: AbstractUoW = Provide[Container.domain_vector_collection_uow],
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client
        self.domain_vector_collection_uow = domain_vector_collection_uow

    async def handle(self, request: DocReadAllQuery) -> list[VectorChromaDocument]:
        with self.domain_vector_collection_uow as uow:
            vec_col_obj = uow.repository.read(request.id_)

            async_vec_db_client = await self.async_vector_db_client.async_init()
            vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
            collection = await vector_collection_repo.read(vec_col_obj.name)

        async_doc_repo = self.async_document_repository(collection)  # type: ignore
        return await async_doc_repo.read_all(
            limit=request.limit,
            offset=request.offset
        )


class DocCountQuery(BaseModel, GenericQuery[int]):
    id_: int


@Mediator.handler
class DocCountHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
            domain_vector_collection_uow: AbstractUoW = Provide[Container.domain_vector_collection_uow]
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client
        self.domain_vector_collection_uow = domain_vector_collection_uow

    async def handle(self, request: DocCountQuery) -> int:
        with self.domain_vector_collection_uow as uow:
            vec_col_obj = uow.repository.read(request.id_)

            async_vec_db_client = await self.async_vector_db_client.async_init()
            vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
            collection = await vector_collection_repo.read(vec_col_obj.name)

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
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
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
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocPeekQuery) -> list[VectorChromaDocument]:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        return await async_doc_repo.peek()


class DocQuery(BaseModel, GenericQuery[list[VectorChromaDocument]]):
    vec_col_name: str
    query_string: str
    doc_names: list[str] | None
    n_results: int | None


@Mediator.handler
class DocQueryHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocQuery) -> list[VectorChromaDocument]:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        return await async_doc_repo.query(
            query_string=request.query_string,
            doc_names=request.doc_names,
            n_results=request.n_results
        )


class DocListDocsQuery(BaseModel, GenericQuery[list[str]]):
    vec_col_name: str


@Mediator.handler
class DocListDocsHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_document_repository: Type[AbstractAsyncDocumentRepository] = Provide[
                Container.async_vector_document_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_document_repository = async_vector_document_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: DocListDocsQuery) -> list[str]:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        collection = await vector_collection_repo.read(request.vec_col_name)
        async_doc_repo = self.async_document_repository(collection)  # type: ignore

        return await async_doc_repo.list_documents()

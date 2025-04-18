from typing import Type, Sequence

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from pydantic import BaseModel

from src.enums import DistanceFunction
from src.adapters.async_vector_client import AbstractAsyncClient
from src.adapters.uow import AbstractUoW
from src.adapters.vector_collection_repository import AbstractAsyncVectorCollectionRepository
from src.di_container import Container
from src.domain.services.embedding_model_builder import EmbeddingModelBuilder
from src.domain.models import VectorCollection


class VecCollectionAddCommand(BaseModel, GenericQuery[VectorCollection]):
    name: str
    embedding_model_id: int
    distance_func: DistanceFunction


@Mediator.handler
class VecCollectionAddHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client],
            domain_vector_collection_uow: AbstractUoW = Provide[Container.domain_vector_collection_uow]
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_vector_db_client = async_vector_db_client
        self.domain_vector_collection_uow = domain_vector_collection_uow

    async def handle(self, request: VecCollectionAddCommand) -> VectorCollection:
        # to rollback domain db changes if vector db storing fails
        with self.domain_vector_collection_uow as uow:
            # storing vector col in domain db
            vec_col_obj = VectorCollection(**request.model_dump())  # type: ignore
            uow.repository.add(vec_col_obj)
            uow.commit()

            # initializing vector db collection and repo
            async_vec_db_client = await self.async_vector_db_client.async_init()
            vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
            await vector_collection_repo.add(
                name=request.name,
                metadata={'hnswspace': request.distance_func.value}
            )

            return vec_col_obj


class VecCollectionReadQuery(BaseModel, GenericQuery[VectorCollection]):
    id_: int


@Mediator.handler
class VecCollectionReadHandler:
    @inject
    def __init__(
            self,
            domain_vector_collection_uow: AbstractUoW = Provide[Container.domain_vector_collection_uow]
    ):
        self.domain_vector_collection_uow = domain_vector_collection_uow

    async def handle(self, request: VecCollectionReadQuery) -> VectorCollection:
        with self.domain_vector_collection_uow as uow:
            return uow.repository.read(request.id_)


class VecCollectionReadAllQuery(BaseModel, GenericQuery[Sequence[VectorCollection]]):
    limit: int | None
    offset: int | None


@Mediator.handler
class VecCollectionReadAllHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client]
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: VecCollectionReadAllQuery) -> Sequence[VectorCollection]:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore

        raw_collections = await vector_collection_repo.read_all(**request.model_dump())

        return list(map(lambda c: VectorCollection(c), raw_collections))


class VecCollectionDeleteCommand(BaseModel, GenericQuery[None]):
    name: str


@Mediator.handler
class VecCollectionDeleteHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client]
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: VecCollectionDeleteCommand) -> None:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore

        await vector_collection_repo.delete(request.name)


class VecCollectionCountQuery(GenericQuery[int]):
    pass


@Mediator.handler
class VecCollectionCountHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client]
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: VecCollectionCountQuery) -> int:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore

        return await vector_collection_repo.count()

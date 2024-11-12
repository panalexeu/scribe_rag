from typing import Type

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from pydantic import BaseModel

from src.enums import DistanceFunction
from src.adapters.async_vector_client import AbstractAsyncClient
from src.adapters.chroma_models import VectorCollection
from src.adapters.uow import AbstractUoW
from src.adapters.vector_collection_repository import AbstractAsyncVectorCollectionRepository
from src.di_container import Container
from src.domain.services.embedding_model_builder import EmbeddingModelBuilder


class VecCollectionAddCommand(BaseModel, GenericQuery[VectorCollection]):
    name: str
    embedding_model_id: int
    distance_func: DistanceFunction | None


@Mediator.handler
class VecCollectionAddHandler:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow],
            embedding_model_builder: EmbeddingModelBuilder = Provide[Container.embedding_model_builder],
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client]
    ):
        self.embedding_model_uow = embedding_model_uow
        self.embedding_model_builder = embedding_model_builder
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: VecCollectionAddCommand) -> VectorCollection:
        # retrieving values from non vector db
        with self.embedding_model_uow as uow:
            embedding_model = uow.repository.read(request.embedding_model_id)

        # initializing async vector db collection and repo
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore
        embedding_func = self.embedding_model_builder.build(embedding_model)

        raw_collection = await vector_collection_repo.add(
            name=request.name,
            embedding_function=embedding_func,
            metadata={'hnswspace': request.distance_func.value} if request.distance_func is not None else None
        )

        return VectorCollection(raw_collection)


class VecCollectionReadQuery(BaseModel, GenericQuery[VectorCollection]):
    name: str


@Mediator.handler
class VecCollectionReadHandler:
    @inject
    def __init__(
            self,
            async_vector_collection_repository: Type[AbstractAsyncVectorCollectionRepository] = Provide[
                Container.async_vector_collection_repository],
            async_vector_db_client: AbstractAsyncClient = Provide[Container.async_vector_db_client]
    ):
        self.async_vector_collection_repository = async_vector_collection_repository
        self.async_vector_db_client = async_vector_db_client

    async def handle(self, request: VecCollectionReadQuery) -> VectorCollection:
        async_vec_db_client = await self.async_vector_db_client.async_init()
        vector_collection_repo = self.async_vector_collection_repository(async_vec_db_client)  # type: ignore

        raw_collection = await vector_collection_repo.read(request.name)

        return VectorCollection(raw_collection)

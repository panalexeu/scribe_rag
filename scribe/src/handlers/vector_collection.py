from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from pydantic import BaseModel

from src.adapters.codecs import AbstractCodec
from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.adapters.vector_collection_repository import AsyncAbstractVectorCollectionRepository
from src.domain.services.embbeding_model import EmbeddingModelBuilder


class VecCollectionAddCommand(BaseModel, GenericQuery):
    name: str
    distance: str
    embedding_model_id: int


@Mediator.handler
class VecCollectionAddHandler:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow],
            async_vector_collection_repository: AsyncAbstractVectorCollectionRepository = Provide[
                Container.async_vector_collection_repository],
            embedding_model_builder: EmbeddingModelBuilder = Provide[Container.embedding_model_builder]
    ):
        self.embedding_model_uow = embedding_model_uow
        self.async_vector_collection_repository = async_vector_collection_repository
        self.embedding_model_builder = embedding_model_builder

    async def handle(self, request: VecCollectionAddCommand):
        with self.embedding_model_uow as uow:
            embedding_model = uow.repository.read(request.embedding_model_id)

        embedding_func = self.embedding_model_builder.build(embedding_model)

        return await self.async_vector_collection_repository.add(
            name=request.name,
            embedding_function=embedding_func
        )

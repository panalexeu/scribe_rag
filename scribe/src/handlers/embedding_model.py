from typing import Sequence

from mediatr import Mediator, GenericQuery
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.domain.models import EmbeddingModel
from src.enums import EmbeddingModelName
from src.adapters.uow import AbstractUoW


class EmbeddingModelAddCommand(BaseModel, GenericQuery[EmbeddingModel]):
    name: EmbeddingModelName
    api_key_credential_id: int


@Mediator.handler
class EmbeddingModelAddHandler:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow]
    ):
        self.embedding_model_uow = embedding_model_uow

    def handle(self, request: EmbeddingModelAddCommand) -> EmbeddingModel:
        with self.embedding_model_uow as uow:
            embedding_model_obj = EmbeddingModel(**request.model_dump())
            uow.repository.add(embedding_model_obj)
            uow.commit()

            return embedding_model_obj


class EmbeddingModelReadQuery(BaseModel, GenericQuery[EmbeddingModel]):
    id_: int


@Mediator.handler
class EmbeddingModelReadHandler:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow]
    ):
        self.embedding_model_uow = embedding_model_uow

    def handle(self, request: EmbeddingModelReadQuery) -> EmbeddingModel:
        with self.embedding_model_uow as uow:
            return uow.repository.read(request.id_)


class EmbeddingModelReadAllQuery(GenericQuery[Sequence[EmbeddingModel]]):
    def __init__(self, limit: int | None, offset: int | None, **kwargs):
        self.limit = limit
        self.offset = offset
        self.kwargs = kwargs


@Mediator.handler
class EmbeddingModelReadAll:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow]
    ):
        self.embedding_model_uow = embedding_model_uow

    def handle(self, request: EmbeddingModelReadAllQuery) -> Sequence[EmbeddingModel]:
        with self.embedding_model_uow as uow:
            return uow.repository.read_all(
                limit=request.limit,
                offset=request.offset,
                **request.kwargs
            )


class EmbeddingModelUpdateCommand(BaseModel, GenericQuery[EmbeddingModel]):
    id_: int
    name: EmbeddingModelName | None
    api_key_credential_id: int | None


@Mediator.handler
class EmbeddingModelUpdateHandler:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow]
    ):
        self.embedding_model_uow = embedding_model_uow

    def handle(self, request: EmbeddingModelUpdateCommand) -> EmbeddingModel:
        with self.embedding_model_uow as uow:
            upd_item = uow.repository.update(**request.model_dump())
            uow.commit()

            return upd_item


class EmbeddingModelDeleteCommand(BaseModel, GenericQuery[None]):
    id_: int


@Mediator.handler
class EmbeddingModelDeleteHandler:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow]
    ):
        self.embedding_model_uow = embedding_model_uow

    def handle(self, request: EmbeddingModelDeleteCommand) -> None:
        with self.embedding_model_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()


class EmbeddingModelCountQuery(BaseModel, GenericQuery[int]):
    pass


@Mediator.handler
class EmbeddingModelCountHandler:
    @inject
    def __init__(
            self,
            embedding_model_uow: AbstractUoW = Provide[Container.embedding_model_uow]
    ):
        self.embedding_model_uow = embedding_model_uow

    def handle(self, request: EmbeddingModelCountQuery) -> int:
        with self.embedding_model_uow as uow:
            return uow.repository.count()

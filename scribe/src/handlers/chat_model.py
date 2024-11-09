from typing import Sequence

from pydantic import BaseModel
from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.enums import ChatModelName
from src.domain.models import ChatModel
from src.adapters.uow import AbstractUoW


class ChatModelAddCommand(BaseModel, GenericQuery[ChatModel]):
    name: ChatModelName
    temperature: float | None
    top_p: float | None
    base_url: str | None
    max_tokens: int | None
    max_retries: int | None
    stop_sequences: list[str] | None


@Mediator.handler
class ChatModelAddHandler:
    @inject
    def __init__(
            self,
            chat_model_uow: AbstractUoW = Provide[Container.chat_model_uow]
    ):
        self.chat_model_uow = chat_model_uow

    def handle(self, request: ChatModelAddCommand) -> ChatModel:
        with self.chat_model_uow as uow:
            chat_model_obj = ChatModel(**request.model_dump())
            uow.repository.add(chat_model_obj)
            uow.commit()

            return chat_model_obj


class ChatModelReadQuery(BaseModel, GenericQuery[ChatModel]):
    id_: int


@Mediator.handler
class ChatModelReadHandler:
    @inject
    def __init__(
            self,
            chat_model_uow: AbstractUoW = Provide[Container.chat_model_uow]
    ):
        self.chat_model_uow = chat_model_uow

    def handle(self, request: ChatModelReadQuery) -> ChatModel:
        with self.chat_model_uow as uow:
            return uow.repository.read(request.id_)


class ChatModelReadAllQuery(GenericQuery[Sequence[ChatModel]]):
    def __init__(
            self,
            limit: int | None,
            offset: int | None,
            **kwargs
    ):
        self.limit = limit
        self.offset = offset
        self.kwargs = kwargs


@Mediator.handler
class ChatModelReadAllHandler:
    @inject
    def __init__(
            self,
            chat_model_uow: AbstractUoW = Provide[Container.chat_model_uow]
    ):
        self.chat_model_uow = chat_model_uow

    def handle(self, request: ChatModelReadAllQuery) -> Sequence[ChatModel]:
        with self.chat_model_uow as uow:
            return uow.repository.read_all(
                limit=request.limit,
                offset=request.offset,
                **request.kwargs
            )


class ChatModelUpdateCommand(GenericQuery[ChatModel]):
    def __init__(self, id_: int, **kwargs):
        self.id_ = id_
        self.kwargs = kwargs


@Mediator.handler
class ChatModelUpdateHandler:
    @inject
    def __init__(
            self,
            chat_model_uow: AbstractUoW = Provide[Container.chat_model_uow]
    ):
        self.chat_model_uow = chat_model_uow

    def handle(self, request: ChatModelUpdateCommand) -> ChatModel:
        with self.chat_model_uow as uow:
            upd_chat_model = uow.repository.update(request.id_, **request.kwargs)
            uow.commit()

            return upd_chat_model


class ChatModelDeleteCommand(BaseModel, GenericQuery[None]):
    id_: int


@Mediator.handler
class ChatModelDeleteHandler:
    @inject
    def __init__(
            self,
            chat_model_uow: AbstractUoW = Provide[Container.chat_model_uow]
    ):
        self.chat_model_uow = chat_model_uow

    def handle(self, request: ChatModelDeleteCommand) -> None:
        with self.chat_model_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()


class ChatModelCountQuery(GenericQuery[int]):
    pass


@Mediator.handler
class ChatModelCountHandler:
    @inject
    def __init__(
            self,
            chat_model_uow: AbstractUoW = Provide[Container.chat_model_uow]
    ):
        self.chat_model_uow = chat_model_uow

    def handle(self, request: ChatModelCountQuery) -> int:
        with self.chat_model_uow as uow:
            return uow.repository.count()

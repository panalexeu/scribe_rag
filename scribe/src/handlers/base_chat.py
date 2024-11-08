from typing import Sequence

from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery

from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.models import BaseChat


class BaseChatAddCommand(BaseModel, GenericQuery[BaseChat]):
    name: str
    desc: str
    system_prompt_id: int
    chat_model_id: int
    doc_proc_cnf_id: int


@Mediator.handler
class BaseChatAddHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow]
    ):
        self.base_chat_uow = base_chat_uow

    def handle(self, request: BaseChatAddCommand) -> BaseChat:
        with self.base_chat_uow as uow:
            base_chat_obj = BaseChat(**request.__dict__)
            uow.repository.add(base_chat_obj)
            uow.commit()

            return base_chat_obj


class BaseChatReadQuery(BaseModel, GenericQuery[BaseChat]):
    id_: int


@Mediator.handler
class BaseChatReadHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow]
    ):
        self.base_chat_uow = base_chat_uow

    def handle(self, request: BaseChatReadQuery) -> BaseChat:
        with self.base_chat_uow as uow:
            return uow.repository.read(request.id_)


class BaseChatReadAllQuery(GenericQuery[Sequence[BaseChat]]):
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
class BaseChatReadAllHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow]
    ):
        self.base_chat_uow = base_chat_uow

    def handle(self, request: BaseChatReadAllQuery) -> Sequence[BaseChat]:
        with self.base_chat_uow as uow:
            return uow.repository.read_all(
                offset=request.offset,
                limit=request.limit,
                **request.kwargs
            )


class BaseChatUpdateCommand(GenericQuery[BaseChat]):
    def __init__(self, id_: int, **kwargs):
        self.id_ = id_
        self.kwargs = kwargs


@Mediator.handler
class BaseChatUpdateHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow]
    ):
        self.base_chat_uow = base_chat_uow

    def handle(self, request: BaseChatUpdateCommand) -> BaseChat:
        with self.base_chat_uow as uow:
            upd_item = uow.repository.update(request.id_, **request.kwargs)
            uow.commit()

            return upd_item


class BaseChatDeleteCommand(BaseModel, GenericQuery[None]):
    id_: int


@Mediator.handler
class BaseChatDeleteHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow]
    ):
        self.base_chat_uow = base_chat_uow

    def handle(self, request: BaseChatDeleteCommand) -> None:
        with self.base_chat_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()


class BaseChatCountQuery(GenericQuery[int]):
    pass


@Mediator.handler
class BaseChatCountHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow]
    ):
        self.base_chat_uow = base_chat_uow

    def handle(self, request: BaseChatCountQuery) -> int:
        with self.base_chat_uow as uow:
            return uow.repository.count()

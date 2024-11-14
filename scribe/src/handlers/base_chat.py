from typing import Sequence

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from pydantic import BaseModel

from src.adapters.chat_model import AsyncStream
from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.models import BaseChat
from src.domain.services.chat_model_builder import ChatModelBuilder, ChatPromptTemplateBuilder


class BaseChatAddCommand(BaseModel, GenericQuery[BaseChat]):
    name: str
    desc: str
    chat_model_id: int
    system_prompt_id: int | None
    vec_col_name: str | None


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
            base_chat_obj = BaseChat(**request.model_dump())
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


class BaseChatStreamCommand(BaseModel, GenericQuery[AsyncStream]):
    id_: int
    prompt: str


class InvalidBaseChatObjectError(LookupError):
    def __init__(self, obj_name: str, id_: int):
        super().__init__(f"BaseChat: '{obj_name}' with the id '{id_}' was not found.")


# TODO massive rework is needed here
@Mediator.handler
class BaseChatStreamHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow],
            chat_model_builder_service: ChatModelBuilder = Provide[Container.chat_model_builder_service],
            chat_prompt_template_builder: ChatPromptTemplateBuilder = Provide[Container.chat_prompt_template_builder],
    ):
        self.base_chat_uow = base_chat_uow
        self.chat_model_builder_service = chat_model_builder_service
        self.chat_prompt_template_builder = chat_prompt_template_builder

    def handle(self, request: BaseChatStreamCommand) -> AsyncStream:
        with self.base_chat_uow as uow:
            base_chat: BaseChat = uow.repository.read(request.id_)

        if base_chat.chat_model is None:
            raise InvalidBaseChatObjectError('ChatModel', base_chat.chat_model_id)
        elif base_chat.chat_model.api_key_credential is None:
            raise InvalidBaseChatObjectError('ChatModel.ApiKeyCredential', base_chat.chat_model.api_key_credential_id)

        built_chat_model = self.chat_model_builder_service.build(
            chat_model=base_chat.chat_model,
        )

        prompt = self.chat_prompt_template_builder.build(
            system_prompt=base_chat.system_prompt.content if base_chat.system_prompt is not None else None,
            context=None
        )

        return built_chat_model.async_stream(prompt, input=request.prompt)

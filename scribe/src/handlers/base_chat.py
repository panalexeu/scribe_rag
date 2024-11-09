from typing import Sequence, AsyncIterator

from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery

from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.models import BaseChat
from src.domain.services import ChatModelBuilder, ChatPromptTemplateBuilder
from src.adapters.codecs import AbstractCodec


class BaseChatAddCommand(BaseModel, GenericQuery[BaseChat]):
    name: str
    desc: str
    system_prompt_id: int
    chat_model_id: int
    chat_model_api_key_id: int
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


class BaseChatStreamCommand(BaseModel, GenericQuery[AsyncIterator[str]]):
    id_: int
    prompt: str


@Mediator.handler
class BaseChatStreamHandler:
    @inject
    def __init__(
            self,
            base_chat_uow: AbstractUoW = Provide[Container.base_chat_uow],
            chat_model_builder_service: ChatModelBuilder = Provide[Container.chat_model_builder_service],
            chat_prompt_template_builder: ChatPromptTemplateBuilder = Provide[Container.chat_prompt_template_builder],
            codec: AbstractCodec = Provide[Container.codec]
    ):
        self.base_chat_uow = base_chat_uow
        self.chat_model_builder_service = chat_model_builder_service
        self.chat_prompt_template_builder = chat_prompt_template_builder
        self.codec = codec

    async def handle(self, request: BaseChatStreamCommand) -> AsyncIterator[str]:
        with self.base_chat_uow as uow:
            base_chat: BaseChat = uow.repository.read(request.id_)

        decoded_api_key = self.codec.decode(base_chat.chat_model_api_key.api_key)
        built_chat_model = self.chat_model_builder_service.build(
            chat_model=base_chat.chat_model,
            api_key=decoded_api_key
        )
        prompt = self.chat_prompt_template_builder.build(
            prompt=request.prompt,
            system_prompt=base_chat.system_prompt,
            context=None
        )

        return built_chat_model.async_stream(prompt)  # type: ignore

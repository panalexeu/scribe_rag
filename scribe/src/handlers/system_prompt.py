from typing import Sequence

from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from src.adapters.uow import AbstractUoW
from src.domain.models import SystemPrompt
from src.di_container import Container


class SystemPromptAddCommand(GenericQuery[SystemPrompt]):
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


@Mediator.handler
class SystemPromptAddHandler:
    @inject
    def __init__(
            self,
            system_prompt_uow: AbstractUoW = Provide[Container.system_prompt_uow]
    ):
        self.system_prompt_uow = system_prompt_uow

    def handle(self, request: SystemPromptAddCommand) -> SystemPrompt:
        with self.system_prompt_uow as uow:
            system_prompt_obj = SystemPrompt(**request.__dict__)
            uow.repository.add(system_prompt_obj)
            uow.commit()

            return system_prompt_obj


class SystemPromptReadQuery(GenericQuery[SystemPrompt]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class SystemPromptReadHandler:
    @inject
    def __init__(
            self,
            system_prompt_uow: AbstractUoW = Provide[Container.system_prompt_uow]
    ):
        self.system_prompt_uow = system_prompt_uow

    def handle(self, request: SystemPromptReadQuery) -> SystemPrompt:
        with self.system_prompt_uow as uow:
            return uow.repository.read(request.id_)


class SystemPromptReadAllQuery(GenericQuery[Sequence[SystemPrompt]]):
    def __init__(self, limit: int, offset: int, **kwargs):
        self.limit = limit
        self.offset = offset
        self.kwargs = kwargs


@Mediator.handler
class SystemPromptReadAllHandler:
    @inject
    def __init__(
            self,
            system_prompt_uow: AbstractUoW = Provide[Container.system_prompt_uow]
    ):
        self.system_prompt_uow = system_prompt_uow

    def handle(self, request: SystemPromptReadAllQuery) -> Sequence[SystemPrompt]:
        with self.system_prompt_uow as uow:
            return uow.repository.read_all(
                offset=request.offset,
                limit=request.limit,
                **request.kwargs
            )


class SystemPromptUpdateCommand(GenericQuery[SystemPrompt]):
    def __init__(self, id_: int, **kwargs):
        self.id_ = id_
        self.kwargs = kwargs


@Mediator.handler
class SystemPromptUpdateHandler:
    @inject
    def __init__(
            self,
            system_prompt_uow: AbstractUoW = Provide[Container.system_prompt_uow]
    ):
        self.system_prompt_uow = system_prompt_uow

    def handle(self, request: SystemPromptUpdateCommand) -> SystemPrompt:
        with self.system_prompt_uow as uow:
            upd_item = uow.repository.update(request.id_, **request.kwargs)
            uow.commit()

            return upd_item


class SystemPromptDeleteCommand(GenericQuery[None]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class SystemPromptDeleteHandler:
    @inject
    def __init__(
            self,
            system_prompt_uow: AbstractUoW = Provide[Container.system_prompt_uow]
    ):
        self.system_prompt_uow = system_prompt_uow

    def handle(self, request: SystemPromptDeleteCommand) -> None:
        with self.system_prompt_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()


class SystemPromptCountQuery(GenericQuery[int | None]):
    pass


@Mediator.handler
class SystemPromptCountHandler:
    @inject
    def __init__(
            self,
            system_prompt_uow: AbstractUoW = Provide[Container.system_prompt_uow]
    ):
        self.system_prompt_uow = system_prompt_uow

    def handle(self, request: SystemPromptCountQuery) -> int | None:
        with self.system_prompt_uow as uow:
            return uow.repository.count()

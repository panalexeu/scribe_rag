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


class SystemPromptReadAllQuery(GenericQuery[list[SystemPrompt]]):
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

    def handle(self, request: SystemPromptReadAllQuery):
        with self.system_prompt_uow as uow:
            return uow.repository.read_all(
                offset=request.offset,
                limit=request.limit,
                **request.kwargs
            )

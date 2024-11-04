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

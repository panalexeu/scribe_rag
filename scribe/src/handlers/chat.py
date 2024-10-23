import dataclasses

from mediatr import Mediator
from dependency_injector.wiring import inject, Provide
from mediatr import GenericQuery


@dataclasses.dataclass
class ChatPostRequest(GenericQuery[str]):
    msg: str


@Mediator.handler
class ChatPostHandler:
    @inject
    def __init__(self, dep=Provide['chat_service']):
        self.dep = dep

    def handle(self, request: ChatPostRequest):
        return f'request {request} with dep: {self.dep}'

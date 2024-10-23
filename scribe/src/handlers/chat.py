import dataclasses

from dependency_injector.wiring import Provide, inject
from mediatr import Mediator


@dataclasses.dataclass
class ChatPostRequest:
    msg: str


@Mediator.handler
@inject
def chat_post_handler(request: ChatPostRequest):
    dep = 'mock'
    print(f'request {request} with dep: {dep}')

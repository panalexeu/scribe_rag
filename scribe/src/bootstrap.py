from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Singleton
from mediatr import Mediator

from src.services.chat import print_msg


class Container(DeclarativeContainer):
    mediatr = Singleton(
        Mediator
    )

    chat_service = Callable(
        print_msg,
        'chat service'
    )


def wire_dependencies():
    container = Container()
    container.wire(
        modules=[
            'src.handlers.chat',
            'src.api.routers.chat'
        ]
    )

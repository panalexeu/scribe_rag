from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Singleton
from mediatr import Mediator

from src.services.chat import print_msg


def di_handler_class_manager(HandlerCls: type, is_behaviour=False):
    return HandlerCls()


class Container(DeclarativeContainer):
    mediatr = Singleton(
        Mediator,
        di_handler_class_manager
    )

    chat_service = Callable(
        print_msg,
        'mediator'
    )


def wire_dependencies():
    container = Container()
    container.wire(
        modules=[
            'src.handlers.chat',
            'src.api.routers.chat'
        ]
    )

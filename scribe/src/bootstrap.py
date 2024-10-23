from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable

from .services.chat import print_msg


class Container(DeclarativeContainer):
    printer = Callable(
        print_msg,
        'DI'
    )


def wire_dependencies():
    container = Container()
    container.wire(
        modules=[
            'src.api.routers.chat',
        ]
    )

from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton


class Container(DeclarativeContainer):
    mediatr = Singleton(
        Mediator
    )


def bootstrap():
    container = Container()
    container.wire()

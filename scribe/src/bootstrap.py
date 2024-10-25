from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from src.system.dir import setup_scribe_folder


class Container(DeclarativeContainer):
    mediatr = Singleton(
        Mediator
    )


def bootstrap():
    setup_scribe_folder()

    container = Container()
    container.wire()

from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Callable

from src.system.dir import get_scribe_dir_path, get_scribe_key_file


class Container(DeclarativeContainer):
    scribe_dir = Callable(
        get_scribe_dir_path
    )
    scribe_key_file = Callable(
        get_scribe_key_file
    )

    mediatr = Singleton(
        Mediator
    )


def bootstrap():
    container = Container()
    container.wire()

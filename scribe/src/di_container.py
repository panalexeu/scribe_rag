from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Callable

from src.system.dir import get_scribe_dir_path, get_scribe_key_file, get_scribe_log_dir_path


class Container(DeclarativeContainer):
    scribe_dir = Callable(
        get_scribe_dir_path
    )
    scribe_key_file = Callable(
        get_scribe_key_file
    )
    log_dir = Callable(
        get_scribe_log_dir_path
    )

    mediatr = Singleton(
        Mediator
    )

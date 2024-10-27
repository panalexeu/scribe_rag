from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Callable

from src.system.dir import get_scribe_dir_path, get_scribe_key_file, get_scribe_log_dir_path
from src.system.logging import read_yaml


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
    log_config = Callable(
        read_yaml,
        './log_configs/dev.yaml'
    )

    mediatr = Singleton(
        Mediator
    )

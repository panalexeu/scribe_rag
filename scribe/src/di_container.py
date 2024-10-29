from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Callable

from src.system.dir import get_scribe_dir_path, get_scribe_key_file, get_scribe_log_dir_path
from src.system.logging import read_log_config


class Container(DeclarativeContainer):
    scribe_dir = Callable(
        get_scribe_dir_path,
        dir_name='.scribe'
    )
    scribe_key_file = Callable(
        get_scribe_key_file,
        scribe_dir=scribe_dir(),
        key_name='scribe.key'
    )
    log_dir = Callable(
        get_scribe_log_dir_path,
        scribe_dir=scribe_dir(),
        log_dir_name='logs'
    )
    log_config = Callable(
        read_log_config,
        log_dir=log_dir(),
        config_path='./log_config.yaml',
        log_file_name='scribe.log'
    )

    mediatr = Singleton(
        Mediator
    )

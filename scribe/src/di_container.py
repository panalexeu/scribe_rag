import os

from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Callable
from sqlalchemy.orm import registry

from src.system.dir import get_scribe_dir_path
from src.system.logging import read_log_config


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            'src.handlers'
        ],
        modules=[
            'src.api.start_api',
            'src.adapters.orm_models'
        ]
    )

    scribe_dir = Callable(
        get_scribe_dir_path,
        dir_name='.scribe'
    )
    scribe_key_file = Callable(
        os.path.join,
        scribe_dir(),
        'scribe.key'
    )
    log_dir = Callable(
        os.path.join,
        scribe_dir(),
        'logs'
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
    registry = Singleton(
        registry
    )

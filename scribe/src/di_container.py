import os

from mediatr import Mediator
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Callable, Factory
from sqlalchemy.orm import registry, Session
from sqlalchemy import create_engine

from src.system.dir import get_scribe_dir_path
from src.system.logging import read_log_config
from src.domain.services import EncodeApiKeyCredentialService
from src.adapters.codecs import FernetCodec
from src.api.start_api import start_api


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            'src.handlers'
        ],
        modules=[
            'src.api.start_api'
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
    engine = Callable(
        create_engine,
        url='sqlite:///:memory:',
        echo=True
    )
    start_api = Callable(
        start_api,
        log_config=log_config(),
        reload=True
    )

    mediatr = Singleton(
        Mediator
    )
    registry = Singleton(
        registry
    )
    session = Singleton(
        Session
    )

    api_key_codec = Singleton(
        FernetCodec,

    )

    encode_api_key_service = Factory(
        EncodeApiKeyCredentialService,

    )

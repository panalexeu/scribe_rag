import os

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Callable, Factory
from mediatr import Mediator
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Session

from src.adapters.codecs import FernetCodec
from src.api.start_api import start_api
from src.domain.services import EncodeApiKeyCredentialService
from src.system.dir import get_scribe_dir_path, read_scribe_key
from src.system.logging import read_log_config


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            'src.handlers'
        ],
        modules=[
            'src.api.start_api'
        ]
    )

    mediatr = Singleton(
        Mediator
    )

    # scribe dir setup related dependencies
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
    start_api = Callable(
        start_api,
        log_config=log_config(),
        reload=True
    )

    # key related dependencies
    read_scribe_key = Callable(
        read_scribe_key,
        scribe_key_file()
    )
    gen_key = Callable(
        FernetCodec.gen_key()
    )
    codec = Singleton(
        FernetCodec,
        key=read_scribe_key()
    )

    # services dependencies
    encode_api_key_service = Factory(
        EncodeApiKeyCredentialService,
        codec()
    )

    # sqlalchemy orm related dependencies
    engine = create_engine(
        url='sqlite:///:memory:',
        echo=True
    )
    registry = Singleton(
        registry
    )
    session = Singleton(
        Session,
        engine
    )

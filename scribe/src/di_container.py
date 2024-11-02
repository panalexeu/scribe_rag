import os

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Callable, Factory
from mediatr import Mediator
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Session
from sqlalchemy.pool import StaticPool

from src.adapters.codecs import FernetCodec
from src.api.start_api import start_api
from src.domain.services import EncodeApiKeyCredentialService
from src.domain.models import ApiKeyCredential
from src.system.dir import get_scribe_dir_path, read_scribe_key
from src.system.logging import read_log_config
from src.adapters.repository import SqlAlchemyRepository
from src.adapters.uow import SqlAlchemyUoW


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            'src.handlers',
            'src.api.routers'
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
        scribe_dir,
        'scribe.key'
    )
    log_dir = Callable(
        os.path.join,
        scribe_dir,
        'logs'
    )
    log_config = Callable(
        read_log_config,
        log_dir=log_dir,
        config_path='./log_config.yaml',
        log_file_name='scribe.log'
    )
    start_api = Callable(
        start_api,
        log_config=log_config,
        reload=True
    )

    # scribe key related dependencies
    gen_key = Callable(
        FernetCodec.gen_key
    )
    read_scribe_key = Callable(
        read_scribe_key,
        scribe_key_file
    )
    codec = Factory(
        FernetCodec,
        key=read_scribe_key
    )
    encode_api_key_service = Factory(
        EncodeApiKeyCredentialService,
        codec
    )

    # sqlalchemy orm related dependencies
    registry = Singleton(
        registry
    )
    # Use StaticPool to share a single connection across threads, enabling multithreaded access
    # to a :memory: database in SQLAlchemy with check_same_thread=False.
    engine = Singleton(
        create_engine,
        url='sqlite:///:memory:',
        echo=True,
        poolclass=StaticPool,
        connect_args={'check_same_thread': False}
    )
    # creating on every request a new session (Factory) is better, since we are making for sure, that there is no
    # objects from any previous interactions in the session
    session = Factory(
        Session,
        bind=engine,
        expire_on_commit=True  # clears data when the session is commited
    )

    api_key_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRepository[ApiKeyCredential],
        session=session
    )

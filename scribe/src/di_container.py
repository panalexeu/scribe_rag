import os

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Callable, Factory
from mediatr import Mediator
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Session
from sqlalchemy.pool import StaticPool
from langchain_unstructured.document_loaders import UnstructuredLoader

from src.adapters.codecs import FernetCodec
from src.domain.services import (
    EncodeApiKeyCredentialService,
    LoadDocumentService
)
from src.system.dir import get_scribe_dir_path, read_scribe_key
from src.system.logging import read_log_config
from src.adapters.repository import (
    SqlAlchemyRepository,
    SqlAlchemyRelationRepository
)
from src.adapters.uow import SqlAlchemyUoW
from src.domain.models import (
    ApiKeyCredential,
    SystemPrompt,
    DocProcessingConfig,
    BaseChat
)


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            'src.handlers',
            'src.api.routers'
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
        autoflush=False,
        expire_on_commit=False
    )

    # uow's
    api_key_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRepository[ApiKeyCredential],
        session=session
    )
    system_prompt_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRepository[SystemPrompt],
        session=session
    )
    doc_proc_cnf_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRepository[DocProcessingConfig],
        session=session
    )
    base_chat_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRelationRepository[BaseChat],
        session=session
    )

    # services
    load_document_service = Singleton(
        LoadDocumentService,
        doc_loader=UnstructuredLoader
    )
    encode_api_key_service = Factory(
        EncodeApiKeyCredentialService,
        codec=codec
    )

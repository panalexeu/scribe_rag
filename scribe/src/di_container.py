import os

from chromadb import AsyncHttpClient
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Callable, Factory, Object
from langchain_unstructured.document_loaders import UnstructuredLoader
from mediatr import Mediator
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Session
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

from src.adapters.async_vector_client import ChromaAsyncVectorClient
from src.adapters.codecs import FernetCodec
from src.adapters.repository import (
    SqlAlchemyRepository,
    SqlAlchemyRelationRepository
)
from src.adapters.uow import SqlAlchemyUoW
from src.adapters.vector_collection_repository import (
    AsyncChromaVectorCollectionRepository,
    AsyncChromaDocumentRepository
)
from src.domain.models import (
    ApiKeyCredential,
    SystemPrompt,
    DocProcessingConfig,
    BaseChat,
    ChatModel,
    EmbeddingModel,
    VectorCollection
)
from src.domain.services import (
    EncodeApiKeyCredentialService,
)
from src.domain.services.chat_model_builder import (
    ChatModelBuilder
)
from src.domain.services.chat_prompt_template_builder import ChatPromptTemplateBuilder
from src.domain.services.embedding_model_builder import EmbeddingModelBuilder
from src.domain.services.load_document_service import LoadDocumentService
from src.system.dir import get_scribe_dir_path, read_scribe_key
from src.system.logging import read_log_config


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

    # determining sqlite db to use based on the environment
    load_dotenv()
    env_scribe_db = os.getenv('SCRIBE_DB')
    # if the 'dev' type is provided => in-memory is passed
    # if the 'prod' type is provided => in-file is passed
    match env_scribe_db:
        case 'dev':
            db_url = 'sqlite:///:memory:'
        case 'prod':
            db_url = 'sqlite:///scribe.db'
        case _:
            db_url = 'sqlite:///:memory:'

    # Use StaticPool to share a single connection across threads, enabling multithreaded access
    # to a :memory: database in SQLAlchemy with check_same_thread=False.
    engine = Singleton(
        create_engine,
        url=db_url,
        echo=False,
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

    # chroma vector store
    async_vector_db_client = Factory(
        ChromaAsyncVectorClient,
        AsyncHttpClient,
        port=8001
    )
    async_vector_collection_repository = Object(
        AsyncChromaVectorCollectionRepository
    )
    async_vector_document_repository = Object(
        AsyncChromaDocumentRepository
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
    chat_model_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRelationRepository[ChatModel],
        session=session
    )
    embedding_model_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRelationRepository[EmbeddingModel],
        session=session
    )
    domain_vector_collection_uow = Factory(
        SqlAlchemyUoW,
        repository=SqlAlchemyRelationRepository[VectorCollection],
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
    chat_model_builder_service = Factory(
        ChatModelBuilder,
        codec
    )
    chat_prompt_template_builder = Factory(
        ChatPromptTemplateBuilder
    )
    embedding_model_builder = Factory(
        EmbeddingModelBuilder,
        codec
    )

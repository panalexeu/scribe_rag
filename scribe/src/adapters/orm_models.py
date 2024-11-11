from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    JSON,
    ForeignKey,
    Enum,
    Float
)
from sqlalchemy.orm import (
    registry,
    relationship
)

from src.domain.models import (
    ApiKeyCredential,
    FakeModel,
    SystemPrompt,
    DocProcessingConfig,
    BaseChat,
    ChatModel,
    EmbeddingModel
)
from src.enums import (
    ChatModelName,
    ChunkingStrategy,
    EmbeddingModelName
)


def map_sqlalchemy_models(registry_: registry):
    """
    Maps sqlalchemy models with the domain models.
    """
    fake_table = Table(
        "fake_model",
        registry_.metadata,
        Column("id", Integer, primary_key=True),
        Column("portal_gun", Boolean),
        Column("spaceship", String),
        Column("datetime", DateTime, default=datetime.now)
    )

    api_key_credential_table = Table(
        "api_key_credential",
        registry_.metadata,
        Column("id", Integer, primary_key=True),
        Column("api_key", String, nullable=False),
        Column("name", String, nullable=False),
        Column("datetime", DateTime, default=datetime.now)
    )

    system_prompt_table = Table(
        'system_prompt',
        registry_.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('content', String, nullable=False),
        Column('datetime', DateTime, default=datetime.now)
    )

    doc_processing_config_table = Table(
        'doc_processing_config',
        registry_.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('postprocessors', JSON, nullable=True),
        Column('chunking_strategy', Enum(ChunkingStrategy), nullable=True),
        Column('max_characters', Integer, nullable=True),
        Column('new_after_n_chars', Integer, nullable=True),
        Column('overlap', Integer, nullable=True),
        Column('overlap_all', Boolean, nullable=True),
        Column('datetime', DateTime, default=datetime.now)
    )

    chat_model_table = Table(
        'chat_model',
        registry_.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', Enum(ChatModelName), nullable=False),
        Column('temperature', Float, nullable=True),
        Column('top_p', Float, nullable=True),
        Column('base_url', String, nullable=True),
        Column('max_tokens', Integer, nullable=True),
        Column('max_retries', Integer, nullable=True),
        Column('stop_sequences', JSON, nullable=True),
        Column('datetime', DateTime, default=datetime.now)
    )

    base_chat_table = Table(
        'base_chat',
        registry_.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('desc', String, nullable=False),
        Column('chat_model_id', Integer, ForeignKey('chat_model.id'), nullable=False),
        Column('chat_model_api_key_id', Integer, ForeignKey('api_key_credential.id'), nullable=False),
        Column('system_prompt_id', Integer, ForeignKey('system_prompt.id'), nullable=True),
        Column('doc_proc_cnf_id', Integer, ForeignKey('doc_processing_config.id'), nullable=True),
        Column('datetime', DateTime, default=datetime.now)
    )

    embedding_model_table = Table(
        'embedding_model',
        registry_.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', Enum(EmbeddingModelName), nullable=False),
        Column('api_key_credential_id', Integer, ForeignKey('api_key_credential.id'), nullable=False),
        Column('datetime', DateTime, default=datetime.now)
    )

    registry_.map_imperatively(ApiKeyCredential, api_key_credential_table)
    registry_.map_imperatively(FakeModel, fake_table)
    registry_.map_imperatively(SystemPrompt, system_prompt_table)
    registry_.map_imperatively(DocProcessingConfig, doc_processing_config_table)
    registry_.map_imperatively(ChatModel, chat_model_table)
    registry_.map_imperatively(
        BaseChat,
        base_chat_table,
        properties={
            'system_prompt': relationship(SystemPrompt, uselist=False),
            'chat_model': relationship(ChatModel, uselist=False),
            'chat_model_api_key': relationship(ApiKeyCredential, uselist=False),
            'doc_proc_cnf': relationship(DocProcessingConfig, uselist=False)
        }
    )
    registry_.map_imperatively(
        EmbeddingModel,
        embedding_model_table,
        properties={
            'api_key_credential': relationship(ApiKeyCredential, uselist=False)
        }
    )

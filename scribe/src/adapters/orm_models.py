from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    JSON
)
from sqlalchemy.orm import registry

from src.domain.models import (
    ApiKeyCredential,
    FakeModel,
    SystemPrompt,
    DocProcessingConfig
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
        Column("api_key", String),
        Column("name", String),
        Column("datetime", DateTime, default=datetime.now)
    )

    system_prompt_table = Table(
        'system_prompt',
        registry_.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('content', String),
        Column('datetime', DateTime, default=datetime.now)
    )

    doc_processing_config_table = Table(
        'doc_processing_config',
        registry_.metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('json_config', JSON),
        Column('datetime', DateTime, default=datetime.now)
    )

    registry_.map_imperatively(ApiKeyCredential, api_key_credential_table)
    registry_.map_imperatively(FakeModel, fake_table)
    registry_.map_imperatively(SystemPrompt, system_prompt_table)
    registry_.map_imperatively(DocProcessingConfig, doc_processing_config_table)

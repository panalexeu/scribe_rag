from datetime import date, datetime

from dependency_injector.wiring import Provide, inject
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Date
)
from sqlalchemy.orm import registry

from src.domain.models import (
    ApiKeyCredential
)


@inject
def map_sqlalchemy_models(registry_: registry = Provide['registry']):
    """
    Maps sqlalchemy models with the domain models.
    """
    api_key_credential_table = Table(
        "api_key_credential",
        registry_.metadata,
        Column("id", Integer, primary_key=True),
        Column("api_key", String),
        Column("name", String),
        Column("datetime", Date, default=datetime.now())
    )

    registry_.map_imperatively(ApiKeyCredential, api_key_credential_table)

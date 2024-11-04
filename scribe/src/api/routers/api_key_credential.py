from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator

from src.di_container import Container
from src.handlers.api_key_credential import (
    ApiKeyAddCommand,
    ApiKeyReadQuery,
    ApiKeyReadAllQuery,
    ApiKeyUpdateCommand,
    ApiKeyDeleteCommand
)

from src.domain.models import ApiKeyCredential

router = APIRouter(
    tags=['Api Key Credential'],
    prefix='/api-key'
)


class ApiKeyResponseModel(BaseModel):
    id: int
    name: str
    api_key: str
    datetime: datetime


class ApiKeyAddModel(BaseModel):
    name: str
    api_key: str


class ApiKeyPutModel(BaseModel):
    name: str | None = None


@router.post(
    '/',
    response_model=ApiKeyResponseModel
)
@inject
def api_key_add(
        item: ApiKeyAddModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ApiKeyAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    '/{id_}',
    response_model=ApiKeyResponseModel
)
@inject
def api_key_read(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = ApiKeyReadQuery(id_)
    return mediatr.send(query)


@router.get(
    '/',
    response_model=list[ApiKeyResponseModel]
)
@inject
def api_key_read_all(
        limit: int,
        offset: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = ApiKeyReadAllQuery(limit, offset)
    return mediatr.send(query)


@router.put(
    '/{id_}',
    response_model=ApiKeyResponseModel
)
@inject
def api_key_put(
        id_: int,
        item: ApiKeyPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ApiKeyUpdateCommand(id_, item.name)
    return mediatr.send(command)


@router.delete('/{id_}')
@inject
def api_key_delete(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ApiKeyDeleteCommand(id_)
    mediatr.send(command)

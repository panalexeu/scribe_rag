from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator

from src.di_container import Container
from src.handlers.api_key_credential import (
    ApiKeyAddCommand,
    ApiKeyReadQuery,
    ApiKeyReadAllQuery,
    ApiKeyUpdateCommand
)
from .models import ResponseModel

router = APIRouter(
    tags=['Api Key Credential'],
    prefix='/api-key'
)


class ApiKeyAddModel(BaseModel):
    name: str
    api_key: str


@router.post('/')
@inject
def api_key_add(
        item: ApiKeyAddModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ApiKeyAddCommand(**item.model_dump())
    mediatr.send(command)


@router.get('/{id_}')
@inject
def api_key_read(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = ApiKeyReadQuery(id_)
    res = mediatr.send(query)

    return ResponseModel(res)


@router.get('/')
@inject
def api_key_read_all(
        limit: int,
        offset: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = ApiKeyReadAllQuery(limit, offset)
    res = mediatr.send(query)

    return [ResponseModel(item) for item in res]


class ApiKeyPutModel(BaseModel):
    name: str | None = None


@router.put('/{id_}')
@inject
def api_key_put(
        id_: int,
        item: ApiKeyPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ApiKeyUpdateCommand(id_, item.name)
    mediatr.send(command)


from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator

from src.di_container import Container
from src.handlers.api_key_credential import (
    ApiKeyAddCommand,
    ApiKeyReadQuery
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

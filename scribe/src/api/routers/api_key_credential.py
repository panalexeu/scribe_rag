from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from mediatr import Mediator

from src.di_container import Container
from src.handlers.api_key_credential import (
    ApiKeyAddCommand
)

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
    res = mediatr.send(command)

    return res

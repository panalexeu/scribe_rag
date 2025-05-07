from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from mediatr import Mediator
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi import status

from src.enums import EmbeddingModelName, Device
from src.api.routers.api_key_credential import ApiKeyResponseModel
from src.di_container import Container
from src.handlers.embedding_model import (
    EmbeddingModelAddCommand,
    EmbeddingModelUpdateCommand,
    EmbeddingModelReadQuery,
    EmbeddingModelReadAllQuery,
    EmbeddingModelDeleteCommand,
    EmbeddingModelCountQuery
)

router = APIRouter(
    prefix='/embed-model',
    tags=['Embedding Model']
)


class EmbeddingModelResponseModel(BaseModel):
    id: int
    name: EmbeddingModelName
    device: Device
    api_key_credential_id: int
    api_key_credential: ApiKeyResponseModel | None
    datetime: datetime


class EmbeddingModelPostModel(BaseModel):
    name: EmbeddingModelName
    device: Device
    api_key_credential_id: int


class EmbeddingModelPutModel(BaseModel):
    name: Optional[EmbeddingModelName] = None
    device: Optional[Device] = None
    api_key_credential_id: Optional[int] = None


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=EmbeddingModelResponseModel
)
@inject
def add_embedding_model(
        item: EmbeddingModelPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = EmbeddingModelAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    '/count'
)
@inject
def count_embedding_model(
        mediatr: Mediator = Depends(Provide[Container.mediatr])
) -> int | None:
    query = EmbeddingModelCountQuery()
    return mediatr.send(query)


@router.get(
    '/{id_}',
    response_model=EmbeddingModelResponseModel
)
@inject
def read_embedding_model(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = EmbeddingModelReadQuery(id_=id_)
    return mediatr.send(query)


@router.get(
    '/',
    response_model=list[EmbeddingModelResponseModel]
)
@inject
def read_all_embedding_model(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = EmbeddingModelReadAllQuery(limit, offset)
    return mediatr.send(query)


@router.put(
    '/{id_}',
    response_model=EmbeddingModelResponseModel
)
@inject
def update_embedding_model(
        id_: int,
        upd_item: EmbeddingModelPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = EmbeddingModelUpdateCommand(id_=id_, **upd_item.model_dump())
    return mediatr.send(command)


@router.delete(
    '/{id_}',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
def delete_embedding_model(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = EmbeddingModelDeleteCommand(id_=id_)
    mediatr.send(command)

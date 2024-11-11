from datetime import datetime
from typing import Optional

from mediatr import Mediator
from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from src.di_container import Container
from src.enums import ChatModelName
from src.handlers.chat_model import (
    ChatModelAddCommand,
    ChatModelReadQuery,
    ChatModelReadAllQuery,
    ChatModelUpdateCommand,
    ChatModelDeleteCommand,
    ChatModelCountQuery
)
from src.api.routers.api_key_credential import ApiKeyResponseModel

router = APIRouter(
    prefix='/chat-model',
    tags=['Chat Model']
)


class ChatModelPostModel(BaseModel):
    name: ChatModelName
    api_key_credential_id: int
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    base_url: Optional[str] = None
    max_tokens: Optional[int] = None
    max_retries: Optional[int] = None
    stop_sequences: Optional[list[str]] = None


class ChatModelResponseModel(BaseModel):
    id: int
    name: ChatModelName
    api_key_credential_id: int
    api_key_credential: ApiKeyResponseModel | None
    temperature: float | None
    top_p: float | None
    base_url: str | None
    max_tokens: int | None
    max_retries: int | None
    stop_sequences: str | None
    datetime: datetime


class ChatModelPutModel(BaseModel):
    name: Optional[ChatModelName] = None
    api_key_credential_id: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    base_url: Optional[str] = None
    max_tokens: Optional[int] = None
    max_retries: Optional[int] = None
    stop_sequences: Optional[str] = None


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=ChatModelResponseModel
)
@inject
def add_chat_model(
        item: ChatModelPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ChatModelAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    path='/count'
)
@inject
def count_chat_model(mediatr: Mediator = Depends(Provide[Container.mediatr])) -> int:
    query = ChatModelCountQuery()
    return mediatr.send(query)


@router.get(
    path='/{id_}',
    response_model=ChatModelResponseModel
)
@inject
def read_chat_model(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = ChatModelReadQuery(id_=id_)
    return mediatr.send(query)


@router.get(
    path='/',
    response_model=list[ChatModelResponseModel]
)
@inject
def read_all_chat_model(
        limit: int | None = None,
        offset: int | None = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = ChatModelReadAllQuery(limit, offset)
    return mediatr.send(query)


@router.put(
    path='/{id_}',
    response_model=ChatModelResponseModel
)
@inject
def update_chat_model(
        id_: int,
        upd_item: ChatModelPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ChatModelUpdateCommand(id_=id_, **upd_item.model_dump())
    return mediatr.send(command)


@router.delete(
    path='/{id_}',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
def delete_chat_model(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = ChatModelDeleteCommand(id_=id_)
    mediatr.send(command)

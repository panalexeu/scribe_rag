from datetime import datetime
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends
from fastapi.responses import StreamingResponse
from mediatr import Mediator
from pydantic import BaseModel

from src.api.routers import (
    system_prompt,
    chat_model
)
from src.di_container import Container
from src.handlers.base_chat import (
    BaseChatAddCommand,
    BaseChatReadQuery,
    BaseChatReadAllQuery,
    BaseChatUpdateCommand,
    BaseChatDeleteCommand,
    BaseChatCountQuery,
    BaseChatStreamCommand
)

router = APIRouter(
    prefix='/base-chat',
    tags=['Base Chat']
)


class BaseChatResponseModel(BaseModel):
    id: int
    name: str
    desc: str
    chat_model_id: int
    chat_model: chat_model.ChatModelResponseModel | None
    system_prompt_id: int | None
    system_prompt: system_prompt.SystemPromptResponseModel | None
    vec_col_name: str | None
    datetime: datetime


class BaseChatAddModel(BaseModel):
    name: str
    desc: str
    chat_model_id: int
    system_prompt_id: Optional[int] = None
    vec_col_name: Optional[str] = None


class BaseChatPutModel(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    system_prompt_id: Optional[int] = None
    chat_model_id: Optional[int] = None
    vec_col_name: Optional[str] = None


@router.post(
    '/',
    response_model=BaseChatResponseModel,
    status_code=status.HTTP_201_CREATED
)
@inject
def add_base_chat(
        item: BaseChatAddModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = BaseChatAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    '/count'
)
@inject
def count_base_chat(mediatr: Mediator = Depends(Provide[Container.mediatr])) -> int:
    query = BaseChatCountQuery()
    return mediatr.send(query)


@router.get(
    '/{id_}',
    response_model=BaseChatResponseModel
)
@inject
def read_base_chat(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = BaseChatReadQuery(id_=id_)
    return mediatr.send(query)


@router.get(
    '/',
    response_model=list[BaseChatResponseModel]
)
@inject
def read_all_base_chat(
        limit: int | None = None,
        offset: int | None = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = BaseChatReadAllQuery(limit=limit, offset=offset)
    return mediatr.send(query)


@router.put(
    '/{id_}',
    response_model=BaseChatResponseModel
)
@inject
def update_base_chat(
        id_: int,
        item: BaseChatPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = BaseChatUpdateCommand(id_, **item.model_dump())
    return mediatr.send(command)


@router.delete(
    '/{id_}',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
def delete_base_chat(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = BaseChatDeleteCommand(id_=id_)
    mediatr.send(command)


class BaseChatStreamModel(BaseModel):
    query_string: str
    doc_names: Optional[list[str]] = None
    n_results: Optional[int] = None


@router.post(
    '/{id_}/stream',
)
@inject
async def stream(
        id_: int,
        item: BaseChatStreamModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = BaseChatStreamCommand(id_=id_, **item.model_dump())
    async_generator = await mediatr.send_async(command)

    return StreamingResponse(
        async_generator,  # type: ignore
        media_type='text/event-stream'
    )

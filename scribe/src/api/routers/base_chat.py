from datetime import datetime

from mediatr import Mediator
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.handlers.base_chat import (
    BaseChatAddCommand,
    BaseChatReadQuery,
    BaseChatReadAllQuery,
    BaseChatUpdateCommand,
    BaseChatDeleteCommand,
    BaseChatCountQuery
)

from src.api.routers import (
    system_prompt,
    chat_model,
    doc_processing_cnf
)

router = APIRouter(
    prefix='/base-chat',
    tags=['Base Chat']
)


class BaseChatResponseModel(BaseModel):
    id: int
    name: str
    desc: str
    system_prompt_id: int
    system_prompt: system_prompt.SystemPromptResponseModel | None
    chat_model_id: int
    chat_model: chat_model.ChatModelResponseModel | None
    doc_proc_cnf_id: int
    doc_proc_cnf: doc_processing_cnf.DocProcCnfResponseModel | None
    datetime: datetime


class BaseChatAddModel(BaseModel):
    name: str
    desc: str
    system_prompt_id: int
    chat_model_id: int
    doc_proc_cnf_id: int


class BaseChatPutModel(BaseModel):
    name: str | None = None
    desc: str | None = None
    system_prompt_id: int | None = None
    chat_model_id: int | None = None
    doc_proc_cnf_id: int | None = None


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

from datetime import datetime

from mediatr import Mediator
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.system_prompt import (
    SystemPromptAddCommand,
    SystemPromptReadQuery,
    SystemPromptReadAllQuery,
    SystemPromptUpdateCommand,
    SystemPromptDeleteCommand
)

router = APIRouter(
    prefix='/sys-prompt',
    tags=['System Prompt']
)


class SystemPromptResponseModel(BaseModel):
    id: int
    name: str
    content: str
    datetime: datetime


class SystemPromptPostModel(BaseModel):
    name: str
    content: str


class SystemPromptPutModel(BaseModel):
    name: str | None = None
    content: str | None = None


@router.post(
    path='/',
    response_model=SystemPromptResponseModel,
    status_code=status.HTTP_201_CREATED
)
@inject
def sys_prompt_add(
        item: SystemPromptPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = SystemPromptAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    path='/{id_}',
    response_model=SystemPromptResponseModel
)
@inject
def sys_prompt_read(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = SystemPromptReadQuery(id_)
    return mediatr.send(query)


@router.get(
    path='/',
    response_model=list[SystemPromptResponseModel]
)
@inject
def sys_prompt_read_all(
        limit: int,
        offset: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = SystemPromptReadAllQuery(limit, offset)
    return mediatr.send(query)


@router.put(
    path='/{id_}',
    response_model=SystemPromptResponseModel
)
@inject
def sys_prompt_update(
        id_: int,
        item: SystemPromptPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = SystemPromptUpdateCommand(id_, **item.model_dump())
    return mediatr.send(command)


@router.delete(
    path='/{id_}',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
def sys_prompt_delete(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = SystemPromptDeleteCommand(id_)
    mediatr.send(command)

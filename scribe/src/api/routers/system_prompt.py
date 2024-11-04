from datetime import datetime

from mediatr import Mediator
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.system_prompt import (
    SystemPromptAddCommand
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

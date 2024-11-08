from mediatr import Mediator
from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.chat_model import ChatModelAddCommand
from src.enums import ChatModelName
from .api_key_credential import ApiKeyResponseModel

router = APIRouter(
    prefix='/chat-model',
    tags=['Chat Model']
)


class ChatModelPostModel(BaseModel):
    model_name: ChatModelName
    api_key_credential_id: int
    temperature: float | None = None
    top_p: float | None = None
    base_url: str | None = None
    max_tokens: int | None = None
    max_retries: int | None = None
    stop_sequences: list[str] | None = None


class ChatModelResponseModel(BaseModel):
    model_name: ChatModelName
    api_key_credential_id: int
    api_key_credential: ApiKeyResponseModel | None
    temperature: float | None
    top_p: float | None
    base_url: str | None
    max_tokens: int | None
    max_retries: int | None
    stop_sequences: str | None


class ChatModelPutModel(BaseModel):
    model_name: ChatModelName | None = None
    api_key_credential_id: int | None = None
    temperature: float | None
    top_p: float | None = None
    base_url: str | None = None
    max_tokens: int | None = None
    max_retries: int | None = None
    stop_sequences: list[str] | None = None  # ?


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


# @router.get(
#     path='/count',
# )
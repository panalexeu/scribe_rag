from datetime import datetime

from mediatr import Mediator
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.handlers.vector_store import (
    VectorStoreAddCommand,
    VectorStoreReadQuery,
    VectorStoreReadAllQuery,
    VectorStoreUpdateCommand
)

from src.api.routers import (
    system_prompt,
    api_key_credential,
    doc_processing_cnf
)

router = APIRouter(
    prefix='/vec-store',
    tags=['Vector Store']
)


class VecStoreResponseModel(BaseModel):
    id: int
    name: str
    desc: str
    system_prompt_id: int
    system_prompt: system_prompt.SystemPromptResponseModel | None
    api_key_credential_id: int
    api_key_credential: api_key_credential.ApiKeyResponseModel | None
    doc_proc_cnf_id: int
    doc_proc_cnf: doc_processing_cnf.ReadDocProcCnfResponseModel | None
    datetime: datetime


class VecStoreAddModel(BaseModel):
    name: str
    desc: str
    system_prompt_id: int
    api_key_credential_id: int
    doc_proc_cnf_id: int


class VectorStorePutModel(BaseModel):
    name: str | None = None
    desc: str | None = None
    system_prompt_id: int | None = None
    api_key_credential_id: int | None = None
    doc_proc_cnf_id: int | None = None


@router.post(
    '/',
    response_model=VecStoreResponseModel,
    status_code=status.HTTP_201_CREATED
)
@inject
def vec_store_add(
        item: VecStoreAddModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = VectorStoreAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    '/{id_}',
    response_model=VecStoreResponseModel
)
@inject
def vec_store_read(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = VectorStoreReadQuery(id_)
    return mediatr.send(query)


@router.get(
    '/',
    response_model=list[VecStoreResponseModel]
)
@inject
def vec_store_read_all(
        limit: int,
        offset: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = VectorStoreReadAllQuery(limit=limit, offset=offset)
    return mediatr.send(query)


@router.put(
    '/{id_}',
    response_model=VecStoreResponseModel
)
@inject
def vec_store_update(
        id_: int,
        item: VectorStorePutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = VectorStoreUpdateCommand(id_, **item.model_dump())
    return mediatr.send(command)

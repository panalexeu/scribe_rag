from datetime import datetime

from mediatr import Mediator
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.handlers.vector_store import (
    VectorStoreAddCommand
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

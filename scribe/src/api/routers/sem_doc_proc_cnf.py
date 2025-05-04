from datetime import datetime
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from mediatr import Mediator
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.sem_doc_proc_cnf import (
    SemDocProcCnfAddCommand,
    SemDocProcCnfReadQuery,
    SemDocProcCnfReadAllQuery,
    SemDocProcCnfUpdateCommand,
    SemDocProcCnfDeleteCommand,
    SemDocProcCnfCountQuery
)

router = APIRouter(
    tags=['Semantic Doc Processing Config'],
    prefix='/sem-doc-proc-cnf'
)


class SemDocProcCnfResponseModel(BaseModel):
    id: int
    name: str
    thresh: float
    max_chunk_size: int
    datetime: datetime


class SemDocProcCnfPostModel(BaseModel):
    name: str
    thresh: float
    max_chunk_size: int


class SemDocProcCnfPutModel(BaseModel):
    name: Optional[str] = None
    thresh: Optional[float] = None
    max_chunk_size: Optional[int] = None


@router.post(
    '/',
    response_model=SemDocProcCnfResponseModel,
    status_code=status.HTTP_201_CREATED
)
@inject
def add_sem_doc_proc_cnf(
        item: SemDocProcCnfPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = SemDocProcCnfAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    '/count'
)
@inject
def count_sem_doc_proc_cnf(mediatr: Mediator = Depends(Provide[Container.mediatr])) -> int:
    query = SemDocProcCnfCountQuery()
    return mediatr.send(query)


@router.get(
    '/{id_}',
    response_model=SemDocProcCnfResponseModel,
)
@inject
def read_sem_doc_proc_cnf(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = SemDocProcCnfReadQuery(id_)
    return mediatr.send(query)


@router.get(
    '/',
    response_model=list[SemDocProcCnfResponseModel]
)
@inject
def read_all_sem_doc_proc_cnf(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = SemDocProcCnfReadAllQuery(limit, offset)
    return mediatr.send(query)


@router.put(
    '/{id_}',
    response_model=SemDocProcCnfResponseModel
)
@inject
def update_sem_doc_proc_cnf(
        id_: int,
        item: SemDocProcCnfPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = SemDocProcCnfUpdateCommand(id_, item.model_dump())
    return mediatr.send(command)


@router.delete(
    '/{id_}',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
def delete_sem_doc_proc_cnf(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = SemDocProcCnfDeleteCommand(id_)
    mediatr.send(command)

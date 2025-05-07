import datetime
from typing import Optional

from mediatr import Mediator
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.enums import (
    Postprocessor,
    ChunkingStrategy
)
from src.handlers.doc_processing_cnf import (
    DocProcCnfAddCommand,
    DocProcCnfReadQuery,
    DocProcCnfReadAllQuery,
    DocProcCnfUpdateCommand,
    DocProcCnfDeleteCommand,
    DocProcCountQuery
)

router = APIRouter(
    prefix='/doc-proc-cnf',
    tags=['Doc Processing Config']
)


class DocProcCnfResponseModel(BaseModel):
    id: int
    name: str
    postprocessors: str | None
    chunking_strategy: ChunkingStrategy | None
    max_characters: int | None
    new_after_n_chars: int | None
    overlap: int | None
    overlap_all: bool | None
    datetime: datetime.datetime


class DocProcCnfPostModel(BaseModel):
    name: str
    postprocessors: Optional[list[Postprocessor]] = None
    chunking_strategy: Optional[ChunkingStrategy] = None
    max_characters: Optional[int] = None
    new_after_n_chars: Optional[int] = None
    overlap: Optional[int] = None
    overlap_all: Optional[bool] = None


class DocProcCnfPutModel(BaseModel):
    name: Optional[str] = None
    postprocessors: Optional[str] = None
    chunking_strategy: Optional[ChunkingStrategy] = None
    max_characters: Optional[int] = None
    new_after_n_chars: Optional[int] = None
    overlap: Optional[int] = None
    overlap_all: Optional[bool] = None


@router.post(
    path='/',
    response_model=DocProcCnfResponseModel,
    status_code=status.HTTP_201_CREATED
)
@inject
def add_doc_proc_cnf(
        item: DocProcCnfPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocProcCnfAddCommand(**item.model_dump())
    return mediatr.send(command)


@router.get(
    '/count'
)
@inject
def count_doc_proc_cnf(mediatr: Mediator = Depends(Provide[Container.mediatr])) -> int | None:
    query = DocProcCountQuery()
    return mediatr.send(query)


@router.get(
    path='/{id_}',
    response_model=DocProcCnfResponseModel
)
@inject
def read_doc_proc_cnf(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr]),
):
    query = DocProcCnfReadQuery(id_=id_)
    return mediatr.send(query)


@router.get(
    path='/',
    response_model=list[DocProcCnfResponseModel]
)
@inject
def read_all_doc_proc_cnf(
        limit: int | None = None,
        offset: int | None = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr]),
):
    query = DocProcCnfReadAllQuery(limit=limit, offset=offset)
    return mediatr.send(query)


@router.put(
    path='/{id_}',
    response_model=DocProcCnfResponseModel
)
@inject
def update_doc_proc_cnf(
        id_: int,
        upd_item: DocProcCnfPutModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocProcCnfUpdateCommand(id_, **upd_item.model_dump())
    return mediatr.send(command)


@router.delete(
    path='/{id_}',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
def delete_doc_proc_cnf(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocProcCnfDeleteCommand(id_=id_)
    mediatr.send(command)

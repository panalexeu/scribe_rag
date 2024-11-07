import datetime

from rich import print
from mediatr import Mediator
from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.enums import (
    Postprocessors,
    ChunkingStrategy
)
from src.handlers.doc_processing_cnf import (
    DocProcCnfAddCommand,
    DocProcCnfReadQuery
)

router = APIRouter(
    prefix='/doc-process-cnf',
    tags=['Doc Processing Config']
)


class DocProcCnfResponseModel(BaseModel):
    id: int
    name: str
    postprocessors: list[Postprocessors] | None
    chunking_strategy: ChunkingStrategy | None
    max_characters: int | None
    new_after_n_chars: int | None
    overlap: int | None
    overlap_all: bool | None
    datetime: datetime.datetime


class ReadDocProcCnfResponseModel(BaseModel):
    id: int
    name: str
    json_config: str
    datetime: datetime.datetime


class DocProcCnfPostModel(BaseModel):
    name: str
    postprocessors: list[Postprocessors] | None
    chunking_strategy: ChunkingStrategy | None
    max_characters: int | None
    new_after_n_chars: int | None
    overlap: int | None
    overlap_all: bool | None


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
    path='/{id_}',
    response_model=ReadDocProcCnfResponseModel
)
@inject
def read_doc_proc_cnf(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr]),
):
    query = DocProcCnfReadQuery(id_)
    return mediatr.send(query)

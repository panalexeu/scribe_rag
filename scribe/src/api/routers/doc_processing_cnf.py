import datetime

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
    DocProcCnfAddCommand
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
def add_doc_processing_config(
        item: DocProcCnfPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocProcCnfAddCommand(**item.model_dump())

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile, Form, status
from mediatr import Mediator
from typing import Optional
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.vector_document import (
    DocAddCommand,
    DocReadAllQuery
)

router = APIRouter(
    prefix='/vec-doc',
    tags=['Document']
)


class VectorDocumentResponseModel(BaseModel):
    id_: str
    document: str
    metadata: dict
    embedding: str


@router.post(
    path='/{vec_col_name}',
    status_code=status.HTTP_201_CREATED
)
@inject
async def create_doc(
        vec_col_name: str,
        doc_processing_cnf_id: int = Form(...),
        urls: Optional[list[str]] = Form(None),
        files: Optional[list[UploadFile]] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
) -> None:
    if urls is not None:
        urls = urls[0].split(',')

    if files is not None:
        files = {file.filename: await file.read() for file in files}

    command = DocAddCommand(
        vec_col_name=vec_col_name,
        doc_processing_cnf_id=doc_processing_cnf_id,
        files=files,
        urls=urls
    )

    return await mediatr.send_async(command)  # type: ignore


@router.get(
    path='/{vec_col_name}',
    response_model=list[VectorDocumentResponseModel]
)
@inject
async def read_all_doc(
        vec_col_name: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocReadAllQuery(
        vec_col_name=vec_col_name,
        limit=limit,
        offset=offset
    )

    return await mediatr.send_async(query)

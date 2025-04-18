from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile, Form, status
from mediatr import Mediator
from typing import Optional
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.vector_document import (
    DocAddCommand,
    DocReadAllQuery,
    DocCountQuery,
    DocDeleteCommand,
    DocPeekQuery,
    DocQuery,
    DocListDocsQuery
)

router = APIRouter(
    prefix='/vec-doc',
    tags=['Document']
)


class VectorDocumentResponseModel(BaseModel):
    id_: str
    distance: float | None
    embedding: str
    document: str
    metadata: dict


class VectorDocumentDeleteModel(BaseModel):
    doc_name: str


class VectorQueryPostModel(BaseModel):
    query_string: str
    doc_names: Optional[list[str]] = None
    n_results: Optional[int] = None


@router.post(
    path='/{id_}',
    status_code=status.HTTP_201_CREATED,
    response_model=None
)
@inject
async def create_doc(
        id_: int,
        doc_processing_cnf_id: int = Form(...),
        urls: Optional[list[str]] = Form(None),
        files: Optional[list[UploadFile]] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
) -> None:
    # handle case when urls are provided from interactive docs page
    if urls is not None and len(urls) == 1:
        urls = urls[0].split(',')

    if files is not None:
        files = {file.filename: await file.read() for file in files}

    command = DocAddCommand(
        id_=id_,
        doc_processing_cnf_id=doc_processing_cnf_id,
        files=files,
        urls=urls
    )

    return await mediatr.send_async(command)  # type: ignore


@router.get(
    path='/{id_}',
    response_model=list[VectorDocumentResponseModel]
)
@inject
async def read_all_doc(
        id_: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocReadAllQuery(
        id_=id_,
        limit=limit,
        offset=offset
    )

    return await mediatr.send_async(query)


@router.get(
    path='/{id_}/count',
    response_model=int
)
@inject
async def count_doc(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocCountQuery(id_=id_)
    return await mediatr.send_async(query)


@router.get(
    path='/{id_}/peek',
    response_model=list[VectorDocumentResponseModel]
)
@inject
async def peek_doc(
        id_: int,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocPeekQuery(id_=id_)
    return await mediatr.send_async(query)


@router.delete(
    path='/{id_}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_doc(
        id_: int,
        item: VectorDocumentDeleteModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocDeleteCommand(id_=id_, doc_name=item.doc_name)
    return await mediatr.send_async(command)


@router.post(
    path='/{vec_col_name}/query',
    response_model=list[VectorDocumentResponseModel]
)
@inject
async def query_doc(
        vec_col_name: str,
        item: VectorQueryPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocQuery(
        vec_col_name=vec_col_name,
        **item.model_dump()
    )
    return await mediatr.send_async(query)


@router.get(
    path='/{vec_col_name}/docs',
    response_model=list[str]
)
@inject
async def list_docs_doc(
        vec_col_name: str,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocListDocsQuery(vec_col_name=vec_col_name)
    return await mediatr.send_async(query)

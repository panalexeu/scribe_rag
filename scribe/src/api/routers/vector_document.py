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
    path='/{vec_col_name}',
    status_code=status.HTTP_201_CREATED,
    response_model=None
)
@inject
async def create_doc(
        vec_col_name: str,
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


@router.get(
    path='/{vec_col_name}/count',
    response_model=int
)
@inject
async def count_doc(
        vec_col_name: str,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocCountQuery(vec_col_name=vec_col_name)
    return await mediatr.send_async(query)


@router.get(
    path='/{vec_col_name}/peek',
    response_model=list[VectorDocumentResponseModel]
)
@inject
async def count_doc(
        vec_col_name: str,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = DocPeekQuery(vec_col_name=vec_col_name)
    return await mediatr.send_async(query)


@router.delete(
    path='/{vec_col_name}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_doc(
        vec_col_name: str,
        item: VectorDocumentDeleteModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocDeleteCommand(vec_col_name=vec_col_name, **item.model_dump())
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

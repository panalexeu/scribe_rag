from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends
from mediatr import Mediator
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.vector_collection import (
    VecCollectionAddCommand,
    VecCollectionReadQuery,
    VecCollectionCountQuery,
    VecCollectionDeleteCommand,
    VecCollectionReadAllQuery
)
from src.enums import DistanceFunction

router = APIRouter(
    prefix='/vec-col',
    tags=['Vector Collection']
)


class VectorCollectionPostModel(BaseModel):
    name: str
    embedding_model_id: int
    distance_func: Optional[DistanceFunction] = None


class VectorCollectionResponseModel(BaseModel):
    name: str
    embedding_function: str
    metadata: dict[str, str] | None


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=VectorCollectionResponseModel
)
@inject
async def create_vec_col(
        item: VectorCollectionPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = VecCollectionAddCommand(**item.model_dump())
    return await mediatr.send_async(command)


@router.get(
    '/count'
)
@inject
async def count_vec_col(
        mediatr: Mediator = Depends(Provide[Container.mediatr])
) -> int:
    query = VecCollectionCountQuery()
    return await mediatr.send_async(query)


@router.get(
    '/{name}',
    response_model=VectorCollectionResponseModel
)
@inject
async def read_vec_col(
        name: str,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = VecCollectionReadQuery(name=name)
    return await mediatr.send_async(query)


@router.get(
    '/',
    response_model=list[VectorCollectionResponseModel]
)
@inject
async def read_all_vec_col(
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    query = VecCollectionReadAllQuery(limit=limit, offset=offset)
    return await mediatr.send_async(query)


@router.delete(
    '/{name}',
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_vec_col(
        name: str,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = VecCollectionDeleteCommand(name=name)
    return await mediatr.send_async(command)

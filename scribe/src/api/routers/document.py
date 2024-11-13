from fastapi import APIRouter
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

router = APIRouter(
    prefix='/doc',
    tags=['Document']
)


class DocPostModel(BaseModel):
    ...


@router.post(
    path='/',
)
@inject
async def create_doc():
    pass

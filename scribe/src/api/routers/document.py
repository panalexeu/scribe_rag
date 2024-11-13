from mediatr import Mediator
from fastapi import APIRouter, Depends, UploadFile
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel

from src.di_container import Container
from src.handlers.document import (
    DocAddModel
)

router = APIRouter(
    prefix='/doc',
    tags=['Document']
)


class DocPostModel(BaseModel):
    vec_col_name: str
    doc_processing_cnf_id: int


@router.post(
    path='/',
)
@inject
async def create_doc(
        files: list[UploadFile],
        item: DocPostModel,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocAddModel(
        **item.model_dump(),
        files={file.filename: await file.read() for file in files}
    )

    return await mediatr.send_async(command)

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile, Form
from mediatr import Mediator
from typing import Optional

from src.di_container import Container
from src.handlers.document import (
    DocAddModel
)

router = APIRouter(
    prefix='/doc',
    tags=['Document']
)


@router.post(
    path='/',
)
@inject
async def create_doc(
        vec_col_name: str = Form(...),
        doc_processing_cnf_id: int = Form(...),
        url: Optional[str] = Form(None),
        files: Optional[list[UploadFile]] = None,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    command = DocAddModel(
        vec_col_name=vec_col_name,
        doc_processing_cnf_id=doc_processing_cnf_id,
        files={file.filename: await file.read() for file in files} if files is not None else files,
        url=url
    )

    return await mediatr.send_async(command)

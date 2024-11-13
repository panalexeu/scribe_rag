from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile, Form, status
from mediatr import Mediator
from typing import Optional

from src.di_container import Container
from src.handlers.document import (
    DocAddModel
)

router = APIRouter(
    prefix='/vec-doc',
    tags=['Document']
)


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
):
    if urls is not None:
        urls = urls[0].split(',')

    if files is not None:
        files = {file.filename: await file.read() for file in files}

    command = DocAddModel(
        vec_col_name=vec_col_name,
        doc_processing_cnf_id=doc_processing_cnf_id,
        files=files,
        urls=urls
    )

    return await mediatr.send_async(command)

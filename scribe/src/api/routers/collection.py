from mediatr import Mediator
from fastapi import APIRouter, Depends, UploadFile
from dependency_injector.wiring import Provide, inject

from src.di_container import Container

router = APIRouter(
    prefix='/collection',
    tags=['Collection']
)


@router.post(
    path='/{collection_name}',
)
@inject
async def collection_add_file(
        collection_name: str,
        file: UploadFile,
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    content = await file.read()
    content_str = content.decode()
    return {
        'filename': file.filename,
        'filesize': file.size,
        'content-type': file.content_type,
        'content': content_str
    }

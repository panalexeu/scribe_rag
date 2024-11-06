from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile, status
from langchain_core.documents import Document
from mediatr import Mediator

from src.di_container import Container
from src.handlers.load_document import LoadDocumentCommand

router = APIRouter(
    prefix='/collection',
    tags=['Collection']
)


@router.post(
    path='/{collection_name}',
    status_code=status.HTTP_201_CREATED,
    response_model=list[Document]
)
@inject
async def collection_add_file(
        files: list[UploadFile],
        mediatr: Mediator = Depends(Provide[Container.mediatr])
):
    # TODO make the loop truly async
    command = LoadDocumentCommand({file.filename: await file.read() for file in files})
    return await mediatr.send_async(command)

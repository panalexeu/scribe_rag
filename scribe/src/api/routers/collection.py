from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile, status
from langchain_core.documents import Document
from mediatr import Mediator

from src.di_container import Container
from src.handlers.document_loader import DocumentLoadCommand

router = APIRouter(
    prefix='/collection',
    tags=['Collection']
)


@router.post(
    path='/{collection_name}',
    status_code=status.HTTP_201_CREATED
)
@inject
async def collection_add_file(
        files: list[UploadFile],
        mediatr: Mediator = Depends(Provide[Container.mediatr])
) -> list[Document]:
    # TODO make the loop truly async
    command = DocumentLoadCommand({file.filename: await file.read() for file in files})
    result = await mediatr.send_async(command)

    return result

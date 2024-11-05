import io
from mediatr import Mediator
from fastapi import APIRouter, Depends, UploadFile
from dependency_injector.wiring import Provide, inject
from langchain_unstructured import UnstructuredLoader
from langchain_core.documents import Document

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
) -> list[Document]:
    bytes_ = await file.read()
    wrapped_bytes = io.BytesIO(bytes_)  # wraps bytes in IO object
    loader = UnstructuredLoader(
        file=wrapped_bytes,
        metadata_filename=file.filename,
    )
    documents = await loader.aload()

    return documents

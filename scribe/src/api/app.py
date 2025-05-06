"""
Defines the FastAPI app, registers routers, and sets up exception handling.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from src.adapters.repository import ItemNotFoundError
from src.adapters.vector_collection_repository import (
    CollectionNameError,
    CollectionNotFoundError
)
from src.bootstrap import bootstrap, shutdown
from src.domain.services.load_document_service import (
    UnsupportedFileFormatError,
    UnsupportedSemanticFileFormatError
)
from .routers import (
    api_key_credential,
    system_prompt,
    doc_processing_cnf,
    base_chat,
    chat_model,
    embedding_model,
    vector_collection,
    vector_document,
    sem_doc_proc_cnf
)
from src.handlers.base_chat import InvalidBaseChatObjectError


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap()  # things to be completed before the app's start-up
    yield
    shutdown()  # things to be completed on shutdown


app = FastAPI(lifespan=lifespan)
app.include_router(api_key_credential.router)
app.include_router(system_prompt.router)
app.include_router(doc_processing_cnf.router)
app.include_router(base_chat.router)
app.include_router(chat_model.router)
app.include_router(embedding_model.router)
app.include_router(vector_collection.router)
app.include_router(vector_document.router)
app.include_router(sem_doc_proc_cnf.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)


@app.get('/')
async def root():
    """Endpoint to verify the server has started successfully."""
    return {'detail': 'beep boop beep'}


@app.exception_handler(RequestValidationError)
async def handle_req_validation_err(req: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors(), 'received_body': exc.body})
    )


@app.exception_handler(ItemNotFoundError)
async def handle_item_not_found_error(req, exc: ItemNotFoundError):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=exc.__str__()
    )


@app.exception_handler(UnsupportedFileFormatError)
async def handle_unsupported_file_format_error(req, exc: UnsupportedFileFormatError):
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=exc.__str__()
    )


@app.exception_handler(UnsupportedSemanticFileFormatError)
async def handle_unsupported_file_format_error(req, exc: UnsupportedSemanticFileFormatError):
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=exc.__str__()
    )


@app.exception_handler(InvalidBaseChatObjectError)
async def handle_invalid_base_chat_obj_err(req, exc: InvalidBaseChatObjectError):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=exc.__str__()
    )


@app.exception_handler(CollectionNameError)
async def handle_collection_name_error(req, exc: CollectionNameError):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=exc.__str__()
    )


@app.exception_handler(CollectionNotFoundError)
async def handle_collection_not_found_error(req, exc: CollectionNotFoundError):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=exc.__str__()
    )

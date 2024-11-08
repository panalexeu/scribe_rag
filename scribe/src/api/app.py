"""
Defines the FastAPI app, registers routers, and sets up exception handling.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from src.bootstrap import bootstrap
from src.adapters.repository import ItemNotFoundError
from src.domain.services import UnsupportedFileFormatError
from .routers import (
    api_key_credential,
    system_prompt,
    collection,
    doc_processing_cnf,
    base_chat
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap()  # things to be completed before the app's start-up
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_key_credential.router)
app.include_router(system_prompt.router)
app.include_router(doc_processing_cnf.router)
app.include_router(base_chat.router)


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

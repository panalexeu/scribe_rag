from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.bootstrap import bootstrap

from .routers import (
    api_key_credential
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap()  # things to be completed before the app's start-up
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(
    api_key_credential.router
)


@app.get('/')
def root():
    return {'msg': 'hello, llama!'}

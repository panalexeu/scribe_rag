from fastapi import FastAPI

from .routers import (
    instruct,
    chat
)

from src.bootstrap import wire_dependencies


def app_factory():
    app_ = FastAPI()
    app_.include_router(instruct.router)
    app_.include_router(chat.router)

    wire_dependencies()

    return app_


app = app_factory()


@app.get('/')
def root():
    return {'msg': 'hello, llama!'}

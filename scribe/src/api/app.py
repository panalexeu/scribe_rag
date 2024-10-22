from fastapi import FastAPI

from .routers import (
    instruct
)

app = FastAPI()
app.include_router(instruct.router)


@app.get('/')
def root():
    return {'msg': 'hello, llama!'}

from fastapi import FastAPI

from src.bootstrap import bootstrap


def app_factory():
    app_ = FastAPI()

    bootstrap()

    return app_


app = app_factory()


@app.get('/')
def root():
    return {'msg': 'hello, llama!'}

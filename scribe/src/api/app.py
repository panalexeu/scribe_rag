from fastapi import FastAPI


def app_factory():
    app_ = FastAPI()

    return app_


app = app_factory()


@app.get('/')
def root():
    return {'msg': 'hello, llama!'}

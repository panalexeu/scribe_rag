import uvicorn


def start_api(reload=True):
    uvicorn.run(
        app='src.api.app:app',
        host='0.0.0.0',
        reload=reload
    )

import uvicorn


def start_api(log_config: dict, reload=True):
    uvicorn.run(
        app='src.api.app:app',
        host='0.0.0.0',
        reload=reload,
        log_config=log_config,
    )

import uvicorn
from dependency_injector.wiring import Provide, inject

from src.di_container import Container


@inject
def start_api(config: dict = Provide[Container.log_config], reload=True):
    uvicorn.run(
        app='src.api.app:app',
        host='0.0.0.0',
        reload=reload,
        log_config=config,
    )

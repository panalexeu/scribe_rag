from src.di_container import Container
from src.handlers.app_start import AppStartQuery
from src.api.start_api import start_api
from src.system.logging import configure_logging


def bootstrap():
    configure_logging()

    container = Container()
    container.wire(
        modules=[
            'src.handlers.app_start'
        ]
    )
    container.mediatr().send(AppStartQuery())

    start_api()


if __name__ == '__main__':
    bootstrap()

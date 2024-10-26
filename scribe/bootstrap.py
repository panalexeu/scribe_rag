import logging

from src.di_container import Container
from src.handlers.app_start_handler import AppStartQuery
from src.api.start_api import start_api

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def bootstrap():
    container = Container()
    container.wire(
        modules=[
            'src.handlers.app_start_handler'
        ]
    )
    container.mediatr().send(AppStartQuery())

    start_api()


if __name__ == '__main__':
    bootstrap()

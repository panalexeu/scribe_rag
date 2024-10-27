from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.api.start_api import start_api
from src.system.logging import configure_logging


def bootstrap():
    container = Container()
    container.wire(
        modules=[
            'src.handlers.scribe_dir_setup',
            'src.system.logging',
            'src.api.start_api'
        ]
    )

    configure_logging()
    container.mediatr().send(ScribeDirSetupQuery())
    start_api()


if __name__ == '__main__':
    bootstrap()

import logging

from dotenv import load_dotenv

from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.api.start_api import start_api


def bootstrap():
    load_dotenv()

    container = Container()
    container.wire(
        modules=[
            'src.handlers.scribe_dir_setup',
            'src.system.logging',
            'src.api.start_api'
        ]
    )

    logging.config.dictConfig(container.log_config())
    container.mediatr().send(ScribeDirSetupQuery())
    start_api()


if __name__ == '__main__':
    bootstrap()

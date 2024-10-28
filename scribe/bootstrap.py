import logging

from dotenv import load_dotenv

from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.api.start_api import start_api


def bootstrap():
    container = Container()
    container.wire(
        modules=[
            'src.handlers.scribe_dir_setup',
            'src.system.logging',
            'src.api.start_api'
        ]
    )

    container.mediatr().send(ScribeDirSetupQuery())

    logging.config.dictConfig(container.log_config())
    logging.info('Scribe bootstrap complete.')

    start_api()


if __name__ == '__main__':
    bootstrap()

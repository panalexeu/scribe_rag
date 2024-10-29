import logging

from src.api.start_api import start_api
from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.adapters.orm_models import map_orm_models


def bootstrap():
    container = Container()
    container.wire(
        modules=[
            'src.handlers.scribe_dir_setup',
            'src.system.logging',
            'src.api.start_api',
            'src.adapters.orm_models'
        ]
    )

    container.mediatr().send(ScribeDirSetupQuery())

    logging.config.dictConfig(container.log_config())
    logging.info('Scribe bootstrap complete.')

    map_orm_models()
    start_api()


if __name__ == '__main__':
    bootstrap()

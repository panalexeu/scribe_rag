import logging

from src.api.start_api import start_api
from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.adapters.orm_models import map_sqlalchemy_models


def bootstrap():
    """
    Sets up scribe directory, logs, key file, maps orm models and starts api.
    """

    container = Container()
    container.mediatr().send(ScribeDirSetupQuery())

    log_config = container.log_config()
    logging.config.dictConfig(log_config)
    logging.info('Scribe bootstrap complete.')

    map_sqlalchemy_models()
    start_api()


if __name__ == '__main__':
    bootstrap()

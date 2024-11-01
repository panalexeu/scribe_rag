import logging

from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.adapters.orm_models import map_sqlalchemy_models


def bootstrap():
    """
    Sets up scribe directory, logs, key file, maps orm models and starts api.
    """

    container = Container()
    container.mediatr().send(ScribeDirSetupQuery())

    # configure logging
    log_config = container.log_config()
    logging.config.dictConfig(log_config)
    logging.info('Scribe bootstrap complete.')

    # setting sqlalchemy mapping and creating tables
    registry = container.registry()
    engine = container.engine()
    map_sqlalchemy_models(registry)
    registry.metadata.create_all(engine)

    # starting fast-api
    container.start_api()


if __name__ == '__main__':
    bootstrap()

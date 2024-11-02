import logging

from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.adapters.orm_models import map_sqlalchemy_models


def bootstrap():
    """
    Sets up scribe directory, logs, key file, maps orm models.
    """
    container = Container()
    container.mediatr().send(ScribeDirSetupQuery())

    # configure logging
    log_config = container.log_config()
    logging.config.dictConfig(log_config)
    logging.info('Scribe bootstrap complete.')

    # setting sqlalchemy mapping and creating tables
    map_sqlalchemy_models(container.registry())
    container.registry().metadata.create_all(container.engine())

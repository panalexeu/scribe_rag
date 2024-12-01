import logging
from logging import config
from subprocess import Popen
from typing import Optional
from dotenv import load_dotenv

from src.adapters.orm_models import map_sqlalchemy_models
from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery

CHROMA_PROCESS: Optional[Popen] = None


def bootstrap():
    """
    Sets up scribe directory, logs, key file, maps orm models.
    """
    container = Container()
    container.mediatr().send(ScribeDirSetupQuery())

    # configure logging
    log_config = container.log_config()
    config.dictConfig(log_config)
    logging.info('Scribe bootstrap complete.')

    # setting sqlalchemy mapping and creating tables
    map_sqlalchemy_models(container.registry())
    container.registry().metadata.create_all(container.engine())


def shutdown():
    pass

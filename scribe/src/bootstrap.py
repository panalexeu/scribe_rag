import logging
import os.path
from logging import config
import subprocess
from typing import Optional
from subprocess import Popen
import shutil

from src.di_container import Container
from src.handlers.scribe_dir_setup import ScribeDirSetupQuery
from src.adapters.orm_models import map_sqlalchemy_models

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

    # starting chroma db
    global CHROMA_PROCESS
    chroma_start_cmd = ['chroma', 'run', '--port', '8001']
    CHROMA_PROCESS = subprocess.Popen(chroma_start_cmd)
    logging.info(f'Started ChromaDB process [{CHROMA_PROCESS.pid}]')


def shutdown():
    """
    Terminates ChromaDB process. Clears ChromaDB directory (in-memory behaviour simulation).
    """

    # terminating chroma db process
    if CHROMA_PROCESS and CHROMA_PROCESS.poll() is None:
        CHROMA_PROCESS.terminate()
        CHROMA_PROCESS.wait()
        logging.info(f'ChromaDB process was successfully terminated [{CHROMA_PROCESS.pid}]')

    # cleaning up chroma db directory
    parent_dir = os.path.dirname(__file__)
    parent_parent_dir = os.path.dirname(parent_dir)
    db_path = os.path.join(parent_parent_dir, 'chroma_data')
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        logging.info(f'Cleared ChromaDB \'{db_path}\' directory')

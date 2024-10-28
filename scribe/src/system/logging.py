import logging
from logging import config

import yaml
import coloredlogs

from dependency_injector.wiring import Provide, inject


def read_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        obj = yaml.safe_load(file.read())
        return obj


@inject
def configure_logging(config_: dict = Provide['log_config'], dev=True):
    if dev:
        config.dictConfig(config_)

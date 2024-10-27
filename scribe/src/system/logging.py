import yaml
from logging import config


def read_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        obj = yaml.safe_load(file.read())
        return obj


def configure_logging(dev=True):
    if dev:
        config.dictConfig(read_yaml('./log_configs/dev.yaml'))

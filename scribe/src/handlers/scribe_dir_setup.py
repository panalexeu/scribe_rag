import logging

from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from src.system.dir import setup_scribe_dir


class ScribeDirSetupQuery(GenericQuery[None]):
    pass


@Mediator.handler
class ScribeDirSetupQueryHandler:
    @inject
    def __init__(
            self,
            scribe_dir: str = Provide['scribe_dir'],
            scribe_key_file: str = Provide['scribe_key_file'],
            log_dir: str = Provide['log_dir']
    ):
        self.scribe_dir = scribe_dir
        self.scribe_key_file = scribe_key_file
        self.log_dir = log_dir

    def handle(self, request: ScribeDirSetupQuery):
        setup_scribe_dir(self.scribe_dir, self.scribe_key_file, self.log_dir)

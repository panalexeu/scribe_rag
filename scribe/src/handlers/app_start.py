import logging

from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from src.system.dir import setup_scribe_dir


class AppStartQuery(GenericQuery[None]):
    pass


@Mediator.handler
class AppStartQueryHandler:
    @inject
    def __init__(
            self,
            scribe_dir: str = Provide['scribe_dir'],
            scribe_key_file: str = Provide['scribe_key_file']
    ):
        self.scribe_dir = scribe_dir
        self.scribe_key_file = scribe_key_file

    def handle(self, request: AppStartQuery):
        logging.info('APP STARTUP COMPLETE')
        setup_scribe_dir(self.scribe_dir, self.scribe_key_file)

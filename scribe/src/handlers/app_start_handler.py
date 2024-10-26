from mediatr import Mediator
from dependency_injector.wiring import inject, Provide

from src.system.dir import setup_scribe_dir


@Mediator.handler
class AppStartHandler:
    @inject
    def __init__(
            self,
            scribe_dir: str = Provide['scribe_dir'],
            scribe_key_file: str = Provide['scribe_key_file']
    ):
        self.scribe_dir = scribe_dir
        self.scribe_key_file = scribe_key_file

    def handle(self):
        setup_scribe_dir(self.scribe_dir, self.scribe_key_file)

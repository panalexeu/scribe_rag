from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from src.system.dir import setup_scribe_dir
from src.di_container import Container


class ScribeDirSetupQuery(GenericQuery[None]):
    pass


@Mediator.handler
class ScribeDirSetupQueryHandler:
    @inject
    def __init__(
            self,
            scribe_dir: str = Provide[Container.scribe_dir],
            scribe_key_file: str = Provide[Container.scribe_key_file],
            log_dir: str = Provide[Container.log_dir],
            key: str = Provide[Container.gen_key]
    ):
        self.scribe_dir = scribe_dir
        self.scribe_key_file = scribe_key_file
        self.log_dir = log_dir
        self.key = key

    def handle(self, request: ScribeDirSetupQuery):
        setup_scribe_dir(self.scribe_dir, self.scribe_key_file, self.log_dir, self.key)

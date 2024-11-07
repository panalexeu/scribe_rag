from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from src.domain.models import DocProcessingConfig
from src.enums import Postprocessors, ChunkingStrategy
from src.adapters.uow import AbstractUoW
from src.di_container import Container


class DocProcCnfAddCommand(GenericQuery[DocProcessingConfig]):
    def __init__(
            self,
            name: str,
            postprocessors: list[Postprocessors] | None,
            chunking_strategy: ChunkingStrategy | None,
            max_characters: int | None,
            new_after_n_chars: int | None,
            overlap: int | None,
            overlap_all: bool | None

    ):
        self.name = name
        self.postprocessors = postprocessors
        self.chunking_strategy = chunking_strategy
        self.max_characters = max_characters
        self.new_after_n_chars = new_after_n_chars
        self.overlap = overlap
        self.overlap_all = overlap_all


@Mediator.handler
class DocProcCnfAddHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow

    def handle(self, request: DocProcCnfAddCommand) -> DocProcessingConfig:
        with self.doc_proc_cnf_uow as uow:
            doc_porc_cnf_obj = DocProcessingConfig(**request.__dict__)
            uow.add(doc_porc_cnf_obj)
            uow.commit()

            return doc_porc_cnf_obj

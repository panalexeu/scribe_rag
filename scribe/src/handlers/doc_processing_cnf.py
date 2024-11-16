from typing import Sequence

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from pydantic import BaseModel

from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.models import DocProcessingConfig
from src.enums import Postprocessor, ChunkingStrategy


class DocProcCnfAddCommand(BaseModel, GenericQuery[DocProcessingConfig]):
    name: str
    postprocessors: list[Postprocessor] | None
    chunking_strategy: ChunkingStrategy | None
    max_characters: int | None
    new_after_n_chars: int | None
    overlap: int | None
    overlap_all: bool | None


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
            doc_porc_cnf_obj = DocProcessingConfig(**request.model_dump())
            uow.repository.add(doc_porc_cnf_obj)
            uow.commit()

            return doc_porc_cnf_obj


class DocProcCnfReadQuery(BaseModel, GenericQuery[DocProcessingConfig]):
    id_: int


@Mediator.handler
class DocProcCnfReadHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow

    def handle(self, request: DocProcCnfReadQuery) -> DocProcessingConfig:
        with self.doc_proc_cnf_uow as uow:
            return uow.repository.read(request.id_)


class DocProcCnfReadAllQuery(GenericQuery[Sequence[DocProcessingConfig]]):
    def __init__(
            self,
            limit: int | None,
            offset: int | None,
            **kwargs
    ):
        self.limit = limit
        self.offset = offset
        self.kwargs = kwargs


@Mediator.handler
class DocProcCnfReadAllHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow

    def handle(self, request: DocProcCnfReadAllQuery) -> Sequence[DocProcessingConfig]:
        with self.doc_proc_cnf_uow as uow:
            return uow.repository.read_all(
                limit=request.limit,
                offset=request.offset,
                **request.kwargs
            )


class DocProcCnfUpdateCommand(GenericQuery[DocProcessingConfig]):
    def __init__(self, id_: int, **kwargs):
        self.id_ = id_
        self.kwargs = kwargs


@Mediator.handler
class DocProcCnfUpdateHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow

    def handle(self, request: DocProcCnfUpdateCommand) -> DocProcessingConfig:
        with self.doc_proc_cnf_uow as uow:
            upd_item: DocProcessingConfig = uow.repository.update(request.id_, **request.kwargs)
            upd_item._normalize_attrs()
            uow.commit()

            return upd_item


class DocProcCnfDeleteCommand(BaseModel, GenericQuery[None]):
    id_: int


@Mediator.handler
class DocProcCnfDeleteHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow

    def handle(self, request: DocProcCnfDeleteCommand) -> None:
        with self.doc_proc_cnf_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()


class DocProcCountQuery(GenericQuery[int]):
    pass


@Mediator.handler
class DocProcCountHandler:
    @inject
    def __init__(
            self,
            doc_proc_cnf_uow: AbstractUoW = Provide[Container.doc_proc_cnf_uow]
    ):
        self.doc_proc_cnf_uow = doc_proc_cnf_uow

    def handle(self, request: DocProcCountQuery) -> int:
        with self.doc_proc_cnf_uow as uow:
            return uow.repository.count()

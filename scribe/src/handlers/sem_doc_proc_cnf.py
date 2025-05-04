from typing import Sequence

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery

from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.models import SemanticDocProcessingConfig


class SemDocProcCnfAddCommand(GenericQuery[SemanticDocProcessingConfig]):
    def __init__(
            self,
            thresh: float,
            max_chunk_size: int
    ):
        self.thresh = thresh
        self.max_chunk_size = max_chunk_size


@Mediator.handler
class SemDocProcCnfAddHandler:
    @inject
    def __init__(
            self,
            sem_doc_proc_cnf_uow: AbstractUoW = Provide[Container.sem_doc_proc_cnf_uow]
    ):
        self.sem_doc_proc_cnf_uow = sem_doc_proc_cnf_uow

    def handle(self, request: SemDocProcCnfAddCommand) -> SemanticDocProcessingConfig:
        with self.sem_doc_proc_cnf_uow as uow:
            sem_doc_proc_cnf = SemanticDocProcessingConfig(**request.__dict__)
            uow.repository.add(sem_doc_proc_cnf)
            uow.commit()

            return sem_doc_proc_cnf


class SemDocProcCnfReadQuery(GenericQuery[SemanticDocProcessingConfig]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class SemDocProcCnfReadHandler:
    @inject
    def __init__(
            self,
            sem_doc_proc_cnf_uow: AbstractUoW = Provide[Container.sem_doc_proc_cnf_uow]
    ):
        self.sem_doc_proc_cnf_uow = sem_doc_proc_cnf_uow

    def handle(self, request: SemDocProcCnfReadQuery):
        with self.sem_doc_proc_cnf_uow as uow:
            return uow.repository.read(request.id_)


class SemDocProcCnfReadAllQuery(GenericQuery[Sequence[SemanticDocProcessingConfig]]):
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
class SemDocProcCnfReadAllHandler:
    @inject
    def __init__(
            self,
            sem_doc_proc_cnf_uow: AbstractUoW = Provide[Container.sem_doc_proc_cnf_uow]
    ):
        self.sem_doc_proc_cnf_uow = sem_doc_proc_cnf_uow

    def handle(self, request: SemDocProcCnfReadAllQuery) -> Sequence[SemanticDocProcessingConfig]:
        with self.sem_doc_proc_cnf_uow as uow:
            return uow.repository.read_all(
                offset=request.offset,
                limit=request.limit,
                **request.kwargs
            )


class SemDocProcCnfUpdateCommand(GenericQuery[SemanticDocProcessingConfig]):
    def __init__(
            self,
            id_: int,
            thresh: float,
            max_chunk_size: int
    ):
        self.id_ = id_
        self.thresh = thresh
        self.max_chunk_size = max_chunk_size


@Mediator.handler
class SemDocProcCnfUpdateHandler:
    @inject
    def __init__(
            self,
            sem_doc_proc_cnf_uow: AbstractUoW = Provide[Container.sem_doc_proc_cnf_uow]
    ):
        self.sem_doc_proc_cnf_uow = sem_doc_proc_cnf_uow

    def handle(self, request: SemDocProcCnfUpdateCommand) -> SemanticDocProcessingConfig:
        with self.sem_doc_proc_cnf_uow as uow:
            upd_item = uow.repository.update(**request.__dict__)
            uow.commit()

            return upd_item


class SemDocProcCnfDeleteCommand(GenericQuery[None]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class SemDocProcCnfDeleteHandler:
    @inject
    def __init__(
            self,
            sem_doc_proc_cnf_uow: AbstractUoW = Provide[Container.sem_doc_proc_cnf_uow]
    ):
        self.sem_doc_proc_cnf_uow = sem_doc_proc_cnf_uow

    def handle(self, request: SemDocProcCnfDeleteCommand) -> None:
        with self.sem_doc_proc_cnf_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()


class SemDocProcCnfCountQuery(GenericQuery[int]):
    pass


@Mediator.handler
class SemDocProcCnfCountHandler:
    @inject
    def __init__(
            self,
            sem_doc_proc_cnf_uow: AbstractUoW = Provide[Container.sem_doc_proc_cnf_uow]
    ):
        self.sem_doc_proc_cnf_uow = sem_doc_proc_cnf_uow

    def handle(self, request: SemDocProcCnfCountQuery) -> int:
        with self.sem_doc_proc_cnf_uow as uow:
            return uow.repository.count()

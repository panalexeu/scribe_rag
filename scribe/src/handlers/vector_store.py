from typing import Sequence

from mediatr import Mediator, GenericQuery
from dependency_injector.wiring import inject, Provide

from src.di_container import Container
from src.domain.models import VectorStore
from src.adapters.uow import AbstractUoW, SqlAlchemyUoW


class VectorStoreAddCommand(GenericQuery[VectorStore]):
    def __init__(
            self,
            name: str,
            desc: str,
            system_prompt_id: int,
            api_key_credential_id: int,
            doc_proc_cnf_id: int,
    ):
        self.name = name
        self.desc = desc
        self.system_prompt_id = system_prompt_id
        self.api_key_credential_id = api_key_credential_id
        self.doc_proc_cnf_id = doc_proc_cnf_id


@Mediator.handler
class VectorStoreAddHandler:
    @inject
    def __init__(
            self,
            vector_store_uow: AbstractUoW = Provide[Container.vector_store_uow]
    ):
        self.vector_store_uow = vector_store_uow

    def handle(self, request: VectorStoreAddCommand) -> VectorStore:
        with self.vector_store_uow as uow:
            vector_store_obj = VectorStore(**request.__dict__)
            uow.repository.add(vector_store_obj)
            uow.commit()

            return vector_store_obj


class VectorStoreReadQuery(GenericQuery[VectorStore]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class VectorStoreReadHandler:
    @inject
    def __init__(
            self,
            vector_store_uow: AbstractUoW = Provide[Container.vector_store_uow]
    ):
        self.vector_store_uow = vector_store_uow

    def handle(self, request: VectorStoreReadQuery) -> VectorStore:
        with self.vector_store_uow as uow:
            return uow.repository.read(request.id_)


class VectorStoreReadAllQuery(GenericQuery[Sequence[VectorStore]]):
    def __init__(
            self,
            limit: int,
            offset: int,
            **kwargs
    ):
        self.limit = limit
        self.offset = offset
        self.kwargs = kwargs


@Mediator.handler
class VectorStoreReadAllHandler:
    @inject
    def __init__(
            self,
            vector_store_uow: AbstractUoW = Provide[Container.vector_store_uow]
    ):
        self.vector_store_uow = vector_store_uow

    def handle(self, request: VectorStoreReadAllQuery) -> Sequence[VectorStore]:
        with self.vector_store_uow as uow:
            return uow.repository.read_all(
                offset=request.offset,
                limit=request.limit,
                **request.kwargs
            )


class VectorStoreUpdateCommand(GenericQuery[VectorStore]):
    def __init__(self, id_: int, **kwargs):
        self.id_ = id_
        self.kwargs = kwargs


@Mediator.handler
class VectorStoreUpdateHandler:
    @inject
    def __init__(
            self,
            vector_store_uow: AbstractUoW = Provide[Container.vector_store_uow]
    ):
        self.vector_store_uow = vector_store_uow

    def handle(self, request: VectorStoreUpdateCommand) -> VectorStore:
        with self.vector_store_uow as uow:
            upd_item = uow.repository.update(request.id_, **request.kwargs)
            uow.commit()

            return upd_item


class VectorStoreDeleteCommand(GenericQuery[None]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class VectorStoreDeleteHandler:
    @inject
    def __init__(
            self,
            vector_store_uow: AbstractUoW = Provide[Container.vector_store_uow]
    ):
        self.vector_store_uow = vector_store_uow

    def handle(self, request: VectorStoreDeleteCommand) -> None:
        with self.vector_store_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()

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
            vector_store_uow: SqlAlchemyUoW = Provide[Container.vector_store_uow]
    ):
        self.vector_store_uow = vector_store_uow

    def handle(self, request: VectorStoreAddCommand) -> VectorStore:
        with self.vector_store_uow as uow:
            vector_store_obj = VectorStore(**request.__dict__)
            uow.repository.add(vector_store_obj)
            uow.commit()

            return vector_store_obj

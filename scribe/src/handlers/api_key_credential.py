from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery

from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.models import ApiKeyCredential
from src.domain.services import EncodeApiKeyCredentialService


class ApiKeyAddCommand(GenericQuery[None]):
    def __init__(
            self,
            name: str,
            api_key: str
    ):
        self.name = name
        self.api_key = api_key


class ApiKeyReadQuery(GenericQuery[ApiKeyCredential]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class ApiKeyCredAddHandler:

    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow],
            encode_api_key_service: EncodeApiKeyCredentialService = Provide[Container.encode_api_key_service]
    ):
        self.api_key_uow = api_key_uow
        self.encode_api_key_service = encode_api_key_service

    def handle(self, request: ApiKeyAddCommand):
        with self.api_key_uow as uow:
            api_key_obj = ApiKeyCredential(**request.__dict__)
            self.encode_api_key_service.encode(api_key_obj)
            uow.repository.add(api_key_obj)

            uow.commit()


@Mediator.handler
class ApiKeyReadHandler:
    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow]
    ):
        self.api_key_uow = api_key_uow

    def handle(self, request: ApiKeyReadQuery):
        with self.api_key_uow as uow:
            return uow.repository.read(request.id_)

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from sqlalchemy.orm import Session

from src.adapters.repository import AbstractRepository
from src.di_container import Container
from src.domain.models import ApiKeyCredential
from src.domain.services import EncodeApiKeyCredentialService
from src.adapters.uow import AbstractUoW


class ApiKeyAddCommand(GenericQuery[ApiKeyCredential]):
    name: str
    api_key: str


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

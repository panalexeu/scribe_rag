from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery

from src.domain.models import ApiKeyCredential
from src.adapters.repository import AbstractRepository
from src.adapters.codecs import AbstractCodec


class ApiKeyAddCommand(GenericQuery[ApiKeyCredential]):
    name: str
    api_key: str


@Mediator.handler
class ApiKeyCredAddHandler:

    @inject
    def __init__(
            self,
            session=...,
            repository=...,
            api_key_credential_encode_service=...
    ):
        self.session = session
        self.repository = repository
        self.api_key_credential_encode_service = api_key_credential_encode_service

    def handle(self, request: ApiKeyAddCommand):
        with self.session as session:
            api_key_cred = ApiKeyCredential(**request.__dict__)
            self.api_key_credential_encode_service()
            self.repository.add(api_key_cred)

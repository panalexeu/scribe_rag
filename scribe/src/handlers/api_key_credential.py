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
    ):
        ...

    def handle(self, request: ApiKeyAddCommand):
        api_key_cred = ApiKeyCredential(**request.__dict__)
        self.repository.add(api_key_cred)

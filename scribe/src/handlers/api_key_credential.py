from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery
from sqlalchemy.orm import Session

from src.domain.models import ApiKeyCredential
from src.domain.services import EncodeApiKeyCredentialService
from src.adapters.repository import SqlAlchemyRepository
from src.di_container import Container


class ApiKeyAddCommand(GenericQuery[ApiKeyCredential]):
    name: str
    api_key: str


@Mediator.handler
class ApiKeyCredAddHandler:

    @inject
    def __init__(
            self,
            session: Session = Provide[Container.session],
            encode_api_key_service: EncodeApiKeyCredentialService = Provide[Container.encode_api_key_service]
    ):
        self.session = session
        self.encode_api_key_service = encode_api_key_service

    def handle(self, request: ApiKeyAddCommand):
        with self.session as session:
            api_key_cred = ApiKeyCredential(**request.__dict__)
            self.encode_api_key_service.encode(api_key_cred)

            repository = SqlAlchemyRepository[ApiKeyCredential](
                session=session,
                type_T=ApiKeyCredential
            )

            repository.add(api_key_cred)

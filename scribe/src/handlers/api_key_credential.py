from typing import Sequence

from dependency_injector.wiring import inject, Provide
from mediatr import Mediator, GenericQuery

from src.adapters.uow import AbstractUoW
from src.di_container import Container
from src.domain.models import ApiKeyCredential
from src.domain.services import EncodeApiKeyCredentialService


class ApiKeyAddCommand(GenericQuery[ApiKeyCredential]):
    def __init__(
            self,
            name: str,
            api_key: str
    ):
        self.name = name
        self.api_key = api_key


@Mediator.handler
class ApiKeyAddHandler:

    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow],
            encode_api_key_service: EncodeApiKeyCredentialService = Provide[Container.encode_api_key_service]
    ):
        self.api_key_uow = api_key_uow
        self.encode_api_key_service = encode_api_key_service

    def handle(self, request: ApiKeyAddCommand) -> ApiKeyCredential:
        with self.api_key_uow as uow:
            api_key_obj = ApiKeyCredential(**request.__dict__)
            self.encode_api_key_service.encode(api_key_obj)
            uow.repository.add(api_key_obj)
            uow.commit()

            return api_key_obj


class ApiKeyReadQuery(GenericQuery[ApiKeyCredential]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class ApiKeyReadHandler:
    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow]
    ):
        self.api_key_uow = api_key_uow

    def handle(self, request: ApiKeyReadQuery) -> ApiKeyCredential:
        with self.api_key_uow as uow:
            return uow.repository.read(request.id_)


class ApiKeyReadAllQuery(GenericQuery[Sequence[ApiKeyCredential]]):
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
class ApiKeyReadAllHandler:
    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow]
    ):
        self.api_key_uow = api_key_uow

    def handle(self, request: ApiKeyReadAllQuery) -> Sequence[ApiKeyCredential]:
        with self.api_key_uow as uow:
            return uow.repository.read_all(
                offset=request.offset,
                limit=request.limit,
                **request.kwargs
            )


class ApiKeyUpdateCommand(GenericQuery[ApiKeyCredential]):
    def __init__(
            self,
            id_: int,
            name: str | None = None
    ):
        self.id_ = id_
        self.name = name


@Mediator.handler
class ApiKeyUpdateHandler:

    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow],
    ):
        self.api_key_uow = api_key_uow

    def handle(self, request: ApiKeyUpdateCommand) -> ApiKeyCredential:
        with self.api_key_uow as uow:
            upd_item = uow.repository.update(**request.__dict__)
            uow.commit()

            return upd_item


class ApiKeyDeleteCommand(GenericQuery[None]):
    def __init__(self, id_: int):
        self.id_ = id_


@Mediator.handler
class ApiKeyDeleteHandler:
    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow]
    ):
        self.api_key_uow = api_key_uow

    def handle(self, request: ApiKeyDeleteCommand) -> None:
        with self.api_key_uow as uow:
            uow.repository.delete(request.id_)
            uow.commit()


class ApiKeyCountQuery(GenericQuery[int]):
    pass


@Mediator.handler
class ApiKeyCountHandler:
    @inject
    def __init__(
            self,
            api_key_uow: AbstractUoW = Provide[Container.api_key_uow]
    ):
        self.api_key_uow = api_key_uow

    def handle(self, request: ApiKeyCountQuery) -> int:
        with self.api_key_uow as uow:
            return uow.repository.count()

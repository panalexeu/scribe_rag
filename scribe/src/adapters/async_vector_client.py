from abc import ABC
from typing import Callable

from chromadb import AsyncClientAPI


class AbstractAsyncClient(ABC):
    async def async_init(self):
        pass


class ChromaAsyncVectorClient(AbstractAsyncClient):

    def __init__(self, setup_func: Callable, **kwargs):
        self.setup_func = setup_func
        self.kwargs = kwargs

    async def async_init(self) -> AsyncClientAPI:
        return await self.setup_func(**self.kwargs)

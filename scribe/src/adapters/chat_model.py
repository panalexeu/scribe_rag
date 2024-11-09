from typing import AsyncIterator

from abc import ABC
from langchain_core.runnables.base import Runnable


class AbstractChatModel(ABC):

    def stream(self, input_: str):
        pass

    def invoke(self, input_: str):
        pass

    async def async_stream(self, input_: str):
        pass

    async def async_invoke(self, input_: str):
        pass


class LangchainChatModel(AbstractChatModel):
    def __init__(
            self,
            chat_model: Runnable
    ):
        self.chat_model = chat_model

    async def async_stream(self, input_: str) -> AsyncIterator[str]:
        return self.chat_model.astream(input_)

    def stream(self, input_: str):
        raise NotImplementedError

    def invoke(self, input_: str):
        raise NotImplementedError

    async def async_invoke(self, input_: str):
        raise NotImplementedError

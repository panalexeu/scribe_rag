from typing import AsyncIterator

from abc import ABC

import overrides
from langchain_core.runnables.base import Runnable
from langchain_core.prompts import ChatPromptTemplate


class AbstractChatModel(ABC):

    def stream(self, prompt):
        pass

    def invoke(self, prompt):
        pass

    async def async_stream(self, prompt):
        pass

    async def async_invoke(self, prompt):
        pass


class LangchainChatModel(AbstractChatModel):
    def __init__(
            self,
            chat_model: Runnable
    ):
        self.chat_model = chat_model

    def async_stream(
            self,
            prompt: ChatPromptTemplate
    ) -> AsyncIterator[str]:
        return self.chat_model.astream(prompt)

    def stream(self, input_: str):
        raise NotImplementedError

    def invoke(self, input_: str):
        raise NotImplementedError

    async def async_invoke(self, input_: str):
        raise NotImplementedError

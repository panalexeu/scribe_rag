from abc import ABC
from typing import AsyncIterator

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import Runnable


class AbstractChatModel(ABC):

    def stream(self, prompt):
        pass

    def invoke(self, prompt):
        pass

    async def async_stream(self, prompt, **kwargs):
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
            prompt: ChatPromptTemplate,
            **kwargs
    ) -> AsyncIterator[str]:
        """
        :param prompt: ChatPromptTemplate.
        :param kwargs: Keyword arguments that will be passed to the ChatPromptTemplate.
        """
        chain = prompt | self.chat_model
        return chain.astream(kwargs)

    def stream(self, input_: str):
        raise NotImplementedError

    def invoke(self, input_: str):
        raise NotImplementedError

    async def async_invoke(self, input_: str):
        raise NotImplementedError

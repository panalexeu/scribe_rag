from abc import ABC
from typing import AsyncGenerator, AsyncIterator

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import Runnable
from langchain_core.messages.ai import AIMessageChunk

AsyncStream = AsyncGenerator[str, None]


class AbstractChatModel(ABC):

    def stream(self, prompt):
        pass

    def invoke(self, prompt):
        pass

    def async_stream(self, prompt, **kwargs) -> AsyncStream:
        pass

    async def async_invoke(self, prompt):
        pass


class LangchainChatModel(AbstractChatModel):
    def __init__(
            self,
            chat_model: Runnable
    ):
        self.chat_model = chat_model

    @staticmethod
    async def langchain_async_generator_wrapper(iterator: AsyncIterator[AIMessageChunk]) \
            -> AsyncStream:
        async for chunk in iterator:
            yield chunk.content

    def async_stream(
            self,
            prompt: ChatPromptTemplate,
            **kwargs
    ) -> AsyncStream:
        """
        :param prompt: ChatPromptTemplate.
        :param kwargs: Keyword arguments that will be passed to the ChatPromptTemplate.
        """
        chain = prompt | self.chat_model

        return self.langchain_async_generator_wrapper(chain.astream(kwargs))

    def stream(self, input_: str):
        raise NotImplementedError

    def invoke(self, input_: str):
        raise NotImplementedError

    async def async_invoke(self, input_: str):
        raise NotImplementedError

import json
from base64 import b64encode
from abc import ABC
from typing import AsyncGenerator, AsyncIterator

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import Runnable
from langchain_core.messages.ai import AIMessageChunk

from src.adapters.chroma_models import VectorChromaDocument

AsyncStream = AsyncGenerator[str, None]


class AbstractChatModel(ABC):

    def stream(self, prompt):
        pass

    def invoke(self, prompt):
        pass

    def async_stream(self, prompt, docs_context: list = None, **kwargs) -> AsyncStream:
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
            docs_context: list[VectorChromaDocument] = None,
            **kwargs
    ) -> AsyncStream:
        """
        :param docs_context: list of VectorChromaDocument returned in a stream for additional verbosity
        :param prompt: ChatPromptTemplate.
        :param kwargs: Keyword arguments that will be passed to the ChatPromptTemplate.
        """
        chain = prompt | self.chat_model

        return self.langchain_async_generator_wrapper(chain.astream(kwargs), docs_context)

    @staticmethod
    async def langchain_async_generator_wrapper(
            iterator: AsyncIterator[AIMessageChunk],
            docs_context: list[VectorChromaDocument] | None
    ) -> AsyncStream:
        if docs_context:
            yield f'event: docs\ndata: {json.dumps([doc.__dict__ for doc in docs_context])}\n\n'

        async for chunk in iterator:
            enc_chunk = chunk.content.encode('utf-8')
            b64_chunk = b64encode(enc_chunk)
            dec_chunk = b64_chunk.decode('utf-8')
            yield 'event: response' \
                + f'\ndata: {dec_chunk}' \
                + '\n\n'

    def stream(self, input_: str):
        raise NotImplementedError

    def invoke(self, input_: str):
        raise NotImplementedError

    async def async_invoke(self, input_: str):
        raise NotImplementedError

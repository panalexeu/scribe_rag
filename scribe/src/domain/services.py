import io
from typing import Type

from langchain_anthropic.chat_models import ChatAnthropic
from langchain_cohere.llms import Cohere
from langchain_core.document_loaders.base import BaseLoader, Document
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from src.adapters.chat_model import AbstractChatModel, LangchainChatModel
from src.adapters.codecs import AbstractCodec
from src.domain.models import ChatModel
from src.enums import ChatModelName, ModelProvider
from .models import ApiKeyCredential


class EncodeApiKeyCredentialService:
    """
    Encodes api key of the provided ApiKeyCredential object,
    using the provided codec.
    """

    def __init__(self, codec: AbstractCodec):
        self.codec = codec

    def encode(self, api_key_cred: ApiKeyCredential):
        api_key_cred.api_key = self.codec.encode(api_key_cred.api_key)


class UnsupportedFileFormatError(RuntimeError):
    supported_formats = ['.odt', '.md', 'text files']

    def __init__(self):
        super().__init__(
            f'Unsupported file formate provided. Currently supported are: {', '.join(self.supported_formats)}.'
        )


class LoadDocumentService:
    """
    Service that wraps around langchain_core.document_loaders.base.BaseLoader
    to load documents asynchronously.
    Works with loaders like:
        - langchain_unstructured.document_loaders.UnstructuredLoader;
    """

    def __init__(self, doc_loader: Type[BaseLoader]):
        self.doc_loader = doc_loader

    # TODO make the loop truly async
    async def load_async(self, files: dict[str, bytes]) -> list[Document]:
        """
        :raises UnsupportedFileFormatError:
        """

        all_docs = []
        for filename, bytes_ in files.items():
            wrapped_bytes = io.BytesIO(bytes_)  # <-- BytesIO wrapping around bytes
            document_loader = self.doc_loader(
                file=wrapped_bytes,  # type: ignore
                metadata_filename=filename  # type: ignore
            )

            try:
                docs = await document_loader.aload()
            except ImportError:
                raise UnsupportedFileFormatError

            all_docs.extend(docs)

        return all_docs


class ChatModelBuilder:
    @staticmethod
    def build(
            chat_model: ChatModel,
            api_key: str
    ) -> AbstractChatModel:
        """
        Sets up chat model from the class attributes. Maps attributes for different model providers.
        """
        provider = ChatModelBuilder.determine_model_provider(chat_model.name)
        match provider:
            case ModelProvider.OPENAI:
                model = ChatOpenAI(
                    model_name=chat_model.name.value,
                    temperature=chat_model.temperature if chat_model.temperature is not None else 0.7,
                    top_p=chat_model.top_p,
                    openai_api_base=chat_model.base_url,
                    max_tokens=chat_model.max_tokens,
                    max_retries=chat_model.max_retries if chat_model.max_retries is not None else 2,
                    stop=chat_model.deserialized_stop_sequence,
                    api_key=api_key
                )
                return LangchainChatModel(model)
            case ModelProvider.COHERE:
                model = Cohere(
                    model=chat_model.name.value,
                    temperature=chat_model.temperature,
                    p=chat_model.top_p,
                    base_url=chat_model.base_url,
                    max_tokens=chat_model.max_tokens,
                    max_retries=chat_model.max_retries if chat_model.max_retries is not None else 10,
                    stop=chat_model.deserialized_stop_sequence,
                    cohere_api_key=api_key
                )
                return LangchainChatModel(model)
            case ModelProvider.ANTHROPIC:
                model = ChatAnthropic(
                    model=chat_model.name.value,
                    temperature=chat_model.temperature,
                    top_p=chat_model.top_p,
                    base_url=chat_model.base_url,
                    max_tokens=chat_model.max_tokens if chat_model.max_tokens is not None else 1024,
                    max_retries=chat_model.max_retries if chat_model.max_retries is not None else 2,
                    stop=chat_model.deserialized_stop_sequence,
                    api_key=api_key
                )
                return LangchainChatModel(model)

    @staticmethod
    def determine_model_provider(name: ChatModelName) -> ModelProvider:
        """
        Determines model provider based on the ChatModelName Enum.
        """
        if name in [
            ChatModelName.GPT_4O,
            ChatModelName.GPT_4O_MINI
        ]:
            return ModelProvider.OPENAI
        elif name in [
            ChatModelName.COMMAND,
            ChatModelName.COMMAND_R_PLUS
        ]:
            return ModelProvider.COHERE
        elif name in [
            ChatModelName.CLAUDE_3_5_SONNET_20241022,
            ChatModelName.CLAUDE_3_5_HAIKU_20241022,
            ChatModelName.CLAUDE_3_HAIKU_20240307,
            ChatModelName.CLAUDE_3_OPUS_20240229,
            ChatModelName.CLAUDE_3_SONNET_20240229
        ]:
            return ModelProvider.ANTHROPIC


class ChatPromptTemplateBuilder:

    @staticmethod
    def build(
            prompt: str,
            system_prompt: str | None,
            context: str | None
    ) -> ChatPromptTemplate:
        return ChatPromptTemplate(
            messages=[
                SystemMessage(
                    'You are a helpful AI-assistant. Consider user preferences. Answer to the user questions based on '
                    'the retrieved context.'
                ),
                SystemMessage(f'Context: {context}'),
                HumanMessage(f'Preferences: {system_prompt}'),
                HumanMessage(prompt)
            ]
        )

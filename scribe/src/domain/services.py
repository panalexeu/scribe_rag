import io
from typing import Type
import json

from langchain_core.document_loaders.base import BaseLoader, Document
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_cohere.llms import Cohere
from langchain_anthropic.chat_models import ChatAnthropic

from .models import ApiKeyCredential
from src.adapters.codecs import AbstractCodec
from src.enums import ChatModelName, ModelProvider
from src.adapters.chat_model import AbstractChatModel, LangchainChatModel
from src.domain.models import ChatModel


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
    def __init__(
            self,
            model: ChatModel
    ):
        self.model = model

    def build(self, codec: AbstractCodec) -> AbstractChatModel:
        """
        Sets up chat model from the class attributes. Maps attributes for different model providers.
        """
        decoded_api_key = codec.decode(self.model.api_key_credential.api_key)

        provider = self.determine_model_provider(self.model.name)
        match provider:
            case ModelProvider.OPENAI:
                model = ChatOpenAI(
                    model_name=self.model.name,
                    temperature=self.model.temperature if self.model.temperature is not None else 0.7,
                    top_p=self.model.top_p,
                    openai_api_base=self.model.base_url,
                    max_tokens=self.model.max_tokens,
                    max_retries=self.model.max_retries if self.model.max_retries is not None else 2,
                    stop=self.model.deserialized_stop_sequence,
                    api_key=decoded_api_key
                )
                return LangchainChatModel(model)
            case ModelProvider.COHERE:
                model = Cohere(
                    model=self.model.name,
                    temperature=self.model.temperature,
                    p=self.model.top_p,
                    base_url=self.model.base_url,
                    max_tokens=self.model.max_tokens,
                    max_retries=self.model.max_retries if self.model.max_retries is not None else 10,
                    stop=self.model.deserialized_stop_sequence,
                    cohere_api_key=decoded_api_key
                )
                return LangchainChatModel(model)
            case ModelProvider.ANTHROPIC:
                model = ChatAnthropic(
                    model=self.model.name,
                    temperature=self.model.temperature,
                    top_p=self.model.top_p,
                    base_url=self.model.base_url,
                    max_tokens=self.model.max_tokens if self.model.max_tokens is not None else 1024,
                    max_retries=self.model.max_retries if self.model.max_retries is not None else 2,
                    stop=self.model.deserialized_stop_sequence,
                    api_key=decoded_api_key
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

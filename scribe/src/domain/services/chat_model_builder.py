from langchain_anthropic.chat_models import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models.base import ChatOpenAI

from src.adapters.chat_model import AbstractChatModel, LangchainChatModel
from src.domain.models import ChatModel
from src.enums import ChatModelName, ModelProvider
from src.adapters.codecs import AbstractCodec
from src.adapters.chroma_models import VectorChromaDocument


class ChatModelBuilder:
    def __init__(self, codec: AbstractCodec):
        self.codec = codec

    def build(
            self,
            chat_model: ChatModel,
    ) -> AbstractChatModel:
        """
        Sets up chat model from the class attributes. Maps attributes for different model providers.
        Decodes api key.
        """
        api_key = self.codec.decode(chat_model.api_key_credential.api_key)

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
                model = ChatCohere(
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
            system_prompt: str | None,
            docs: list[VectorChromaDocument] | None
    ) -> ChatPromptTemplate:
        context = None
        if docs is not None:
            context = ChatPromptTemplateBuilder.format_context(docs)

        return ChatPromptTemplate(
            messages=[
                ('system', 'You are a helpful AI-assistant.'),
                ('system', f'Context: {context}'),
                ('human', f'Preferences: {system_prompt}'),
                ('human', '{input}')
            ]
        )

    @staticmethod
    def format_context(docs: list[VectorChromaDocument]) -> str:
        return '\n'.join(list(map(lambda d: d.document, docs)))

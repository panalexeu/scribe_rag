from  chromadb.utils import embedding_functions

from src.adapters.codecs import AbstractCodec
from src.domain.models import EmbeddingModel
from src.enums import (
    EmbeddingModelName,
    ModelProvider
)


class EmbeddingModelBuilder:

    def __init__(self, codec: AbstractCodec):
        self.codec = codec

    def build(
            self,
            embedding_model: EmbeddingModel,
    ) -> embedding_functions.EmbeddingFunction:
        """
        Decodes API-key and forms embedding function.
        """
        provider = EmbeddingModelBuilder.determine_model_provider(embedding_model.name)
        if provider != ModelProvider.LOCAL:
            decoded_api_key = self.codec.decode(embedding_model.api_key_credential.api_key)

            match provider:
                case ModelProvider.OPENAI:
                    return embedding_functions.OpenAIEmbeddingFunction(
                        api_key=decoded_api_key,
                        model_name=embedding_model.name.value
                    )
                case ModelProvider.COHERE:
                    return embedding_functions.CohereEmbeddingFunction(
                        api_key=decoded_api_key,
                        model_name=embedding_model.name.value
                    )

        else:
            return embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model.name.value
            )

    @staticmethod
    def determine_model_provider(name: EmbeddingModelName) -> ModelProvider:
        if name in [
            EmbeddingModelName.TEXT_EMBEDDING_3_SMALL,
        ]:
            return ModelProvider.OPENAI
        elif name in [
            EmbeddingModelName.EMBED_ENGLISH_LIGHT_V3_0,
            EmbeddingModelName.EMBED_MULTILINGUAL_LIGHT_V3_0
        ]:
            return ModelProvider.COHERE
        elif name in [
            EmbeddingModelName.ALL_MINILM_L6_V2,
            EmbeddingModelName.XLM_ROBERTA_UA_DISTILLED
        ]:
            return ModelProvider.LOCAL

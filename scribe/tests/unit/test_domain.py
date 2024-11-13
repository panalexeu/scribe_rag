from copy import copy

from chromadb.utils.embedding_functions import EmbeddingFunction
from langchain_unstructured.document_loaders import UnstructuredLoader
from langchain_core.documents.base import Document

from src.adapters.chat_model import AbstractChatModel
from src.adapters.codecs import FakeCodec
from src.domain.models import (
    ApiKeyCredential,
    DocProcessingConfig,
    ChatModel,
    EmbeddingModel,
    VectorDocument
)
from src.domain.services.load_document_service import LoadDocumentService
from src.domain.services import (
    EncodeApiKeyCredentialService,
    ChatModelBuilder,
)
from src.domain.services.embedding_model_builder import (
    EmbeddingModelBuilder
)
from src.enums import (
    ChunkingStrategy,
    Postprocessor,
    ChatModelName,
    ModelProvider,
    EmbeddingModelName
)
from unstructured.cleaners.core import (
    clean,
    clean_bullets
)


def test_encode_api_key_credential_service():
    api_key_credential = ApiKeyCredential('fake-api', 'fake-key')
    api_key_credential_copy = copy(api_key_credential)

    # encoding the api key and setting encoding service
    codec = FakeCodec('fake-key')
    encode_service = EncodeApiKeyCredentialService(codec)
    encode_service.encode(api_key_credential)

    # only api key is modified by codec encoding
    assert api_key_credential.api_key != api_key_credential_copy.api_key
    assert api_key_credential.name == api_key_credential_copy.name


def test_doc_proc_cnf_serializes_postprocessors():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
        None,
        None,
        None,
        None
    )

    assert isinstance(config.postprocessors, str)


def test_doc_proc_cnf_deserializes_postprocessors():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
        None,
        None,
        None,
        None
    )

    assert config.deserialized_postprocessors == [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS]


def test_doc_proc_cnf_sets_up_chunking_params_as_none_if_no_chunking_strategy_provided():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        None,
        10,
        123,
        12,
        True
    )

    assert config.max_characters is None
    assert config.new_after_n_chars is None
    assert config.overlap is None
    assert config.overlap_all is None


def test_doc_proc_cnf_sets_up_default_values_if_chunking_strategy_provided_but_chunking_params_is_none():
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
        None,
        None,
        None,
        None
    )

    assert config.max_characters == config.new_after_n_chars == 500
    assert config.overlap == 0
    assert config.overlap_all is False


def test_chat_model_serializes_stop_sequences_to_json_string():
    chat_model = ChatModel(
        ChatModelName.GPT_4O,
        1,
        2,
        0.1,
        'web.com',
        1,
        3,
        ['yes', 'no'],
    )

    assert isinstance(chat_model.stop_sequences, str)


def test_chat_model_deserializes_stop_sequences_to_list_str():
    seq = ['yes', 'no']
    chat_model = ChatModel(
        ChatModelName.GPT_4O,
        1,
        2,
        0.1,
        'web.com',
        1,
        3,
        seq
    )

    assert isinstance(chat_model.stop_sequences, str)
    assert chat_model.deserialized_stop_sequence == seq


def test_chat_model_doesnt_serialize_and_deserialize_none_stop_sequence():
    chat_model = ChatModel(
        ChatModelName.GPT_4O,
        1,
        2,
        0.1,
        'web.com',
        1,
        3,
        None
    )

    assert chat_model.stop_sequences is None
    assert chat_model.deserialized_stop_sequence is None


def test_chat_model_builder_correctly_assigns_provider():
    model_names = [ChatModelName.GPT_4O, ChatModelName.COMMAND, ChatModelName.CLAUDE_3_HAIKU_20240307]

    assert list(map(lambda m: ChatModelBuilder.determine_model_provider(m), model_names)) == [ModelProvider.OPENAI,
                                                                                              ModelProvider.COHERE,
                                                                                              ModelProvider.ANTHROPIC]


def test_chat_model_builder_builds_models():
    model = ChatModel(
        ChatModelName.GPT_4O,
        1,
        1,
        None,
        None,
        None,
        None,
        None
    )

    assert isinstance(ChatModelBuilder.build(model, 'fake-key'), AbstractChatModel)


def test_embedding_model_builder_correctly_assigns_provider():
    model_names = [
        EmbeddingModelName.ALL_MINILM_L6_V2,
        EmbeddingModelName.EMBED_ENGLISH_LIGHT_V3_0,
        EmbeddingModelName.TEXT_EMBEDDING_3_SMALL
    ]

    assert list(map(lambda m: EmbeddingModelBuilder.determine_model_provider(m), model_names)) == [ModelProvider.LOCAL,
                                                                                                   ModelProvider.COHERE,
                                                                                                   ModelProvider.OPENAI]


def test_embedding_model_builder_builds_models():
    model = EmbeddingModel(
        name=EmbeddingModelName.ALL_MINILM_L6_V2,
        api_key_credential_id=0
    )

    assert isinstance(EmbeddingModelBuilder(FakeCodec('fake-key')).build(model), EmbeddingFunction)


def test_load_document_service_builds_config():
    loader = LoadDocumentService(UnstructuredLoader)
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        ChunkingStrategy.BASIC,
        150,
        100,
        230,
        False
    )

    res = loader.build_config(doc_proc_cnf=config)
    post_processors = res.pop('post_processors')

    assert {clean.__name__, clean_bullets.__name__} == set((map(lambda p: p.__name__, post_processors)))
    assert res == {
        'chunking_strategy': 'basic',
        'max_characters': 150,
        'new_after_n_chars': 100,
        'overlap': 230,
        'overlap_all': False
    }


def test_load_document_service_builds_config_with_unique_postprocessors():
    loader = LoadDocumentService(UnstructuredLoader)
    config = DocProcessingConfig(
        'fake',
        [Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS,
         Postprocessor.CLEAN, Postprocessor.CLEAN_BULLETS],
        None,
        None,
        None,
        None,
        None,
    )

    res = loader.build_config(doc_proc_cnf=config)
    assert len(res['post_processors']) == 2


def test_load_document_service_maps_doc():
    doc = Document(
        page_content='hey',
        metadata={'filename': 'fake.txt'}
    )
    res = LoadDocumentService.map_doc(doc)

    assert isinstance(res, VectorDocument)
    assert doc.page_content == res.page_content
    assert doc.metadata == res.metadata
    assert res.id_ is not None

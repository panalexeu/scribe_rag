import json
from hashlib import sha224

from src.enums import (
    Postprocessor,
    ChunkingStrategy,
    ChatModelName,
    DistanceFunction,
    EmbeddingModelName,
    Device
)


class FakeModel:

    def __init__(self, portal_gun: bool, spaceship: str):
        self.portal_gun = portal_gun
        self.spaceship = spaceship

    def __repr__(self):
        return f'FakeModel<portal_gun={self.portal_gun}, spaceship={self.spaceship}>'

    def meow(self) -> str:
        return f'Meow! My ship is {self.spaceship}.'


class ApiKeyCredential:

    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key

    def __repr__(self) -> str:
        return f'ApiKeyCredential<name={self.name}, api_key={self.api_key}>'


class SystemPrompt:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content


class DocProcessingConfig:
    """
    Configuration options for processing and chunking Unstructured documents.
    """

    def __init__(
            self,
            name: str,
            postprocessors: list[Postprocessor] | None,
            chunking_strategy: ChunkingStrategy | None,
            max_characters: int | None,
            new_after_n_chars: int | None,
            overlap: int | None,
            overlap_all: bool | None

    ):
        self.name = name
        self.postprocessors = json.dumps(
            list(map(lambda x: x.value, postprocessors))
        ) if postprocessors is not None else None
        self.chunking_strategy = chunking_strategy
        self.max_characters = max_characters
        self.new_after_n_chars = new_after_n_chars
        self.overlap = overlap
        self.overlap_all = overlap_all

        self._normalize_attrs()  # <-- preserving configuration logic

    @property
    def deserialized_postprocessors(self) -> list[Postprocessor] | None:
        return list(map(lambda p: Postprocessor(p), json.loads(self.postprocessors))) \
            if self.postprocessors is not None else None

    def _normalize_attrs(self):
        if self.chunking_strategy is None:
            self.max_characters = None
            self.new_after_n_chars = None
            self.overlap = None
            self.overlap_all = None
        else:
            self.max_characters = 500 if self.max_characters is None else self.max_characters
            self.new_after_n_chars = self.max_characters if self.new_after_n_chars is None else self.new_after_n_chars
            self.overlap = 0 if self.overlap is None else self.overlap
            self.overlap_all = False if self.overlap_all is None else self.overlap_all


class SemanticDocProcessingConfig:
    def __init__(
            self,
            name: str,
            thresh: float,
            max_chunk_size: int
    ):
        self.name = name
        self.thresh = thresh
        self.max_chunk_size = max_chunk_size


class ChatModel:
    api_key_credential: ApiKeyCredential

    def __init__(
            self,
            name: ChatModelName,
            api_key_credential_id: int,
            temperature: float | None,
            top_p: float | None,
            base_url: str | None,
            max_tokens: int | None,
            max_retries: int | None,
            stop_sequences: list[str] | None,
    ):
        self.name = name
        self.api_key_credential_id = api_key_credential_id
        self.temperature = temperature
        self.top_p = top_p
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.stop_sequences = json.dumps(stop_sequences) if stop_sequences is not None else None

    @property
    def deserialized_stop_sequence(self) -> list[str] | None:
        """
        I need this method because of the db mapping 😥. Probably I did some bad designing.
        """
        return json.loads(self.stop_sequences) if self.stop_sequences is not None else None


class EmbeddingModel:
    api_key_credential: ApiKeyCredential

    def __init__(
            self,
            name: EmbeddingModelName,
            device: Device,
            api_key_credential_id: int
    ):
        self.name = name
        self.device = device
        self.api_key_credential_id = api_key_credential_id


class VectorCollection:
    embedding_model: EmbeddingModel
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - populated by db

    def __init__self(
            self,
            name: str,
            distance_func: DistanceFunction,
            embedding_model_id: int
    ):
        self.name = name
        self.distance_func = distance_func
        self.embedding_model_id = embedding_model_id


class VectorDocument:
    def __init__(
            self,
            page_content: str,
            metadata: dict[str, list | str | int | float]
    ):
        self.page_content = page_content
        self.metadata = self.normalize_metadata(metadata)
        self.id_ = sha224(self.page_content.encode()).hexdigest()  # 28 byte hash id (sha224)

    @staticmethod
    def normalize_metadata(dict_: dict):
        metadata = {}
        for key, val in dict_.items():
            if isinstance(val, list):
                metadata[key] = json.dumps(val)
            else:
                metadata[key] = val

        return metadata

    def __repr__(self) -> str:
        return f"VectorDocument<id_={self.id_} page_content='{self.page_content}' metadata={self.metadata}>"


class BaseChat:
    chat_model: ChatModel
    system_prompt: SystemPrompt | None
    vec_col: VectorCollection | None
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - populated by db

    def __init__(
            self,
            name: str,
            desc: str,
            chat_model_id: int,
            system_prompt_id: int | None,
            vec_col_id: int | None
    ):
        self.name = name
        self.desc = desc
        self.system_prompt_id = system_prompt_id
        self.chat_model_id = chat_model_id
        self.vec_col_id = vec_col_id

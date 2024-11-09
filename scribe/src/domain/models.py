import json

from src.enums import (
    Postprocessor,
    ChunkingStrategy,
    ChatModelName
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

        if self.chunking_strategy is None:
            self.max_characters = None
            self.new_after_n_chars = None
            self.overlap = None
            self.overlap_all = None
        else:
            self.max_characters = 500 if max_characters is None else max_characters
            self.new_after_n_chars = self.max_characters if new_after_n_chars is None else new_after_n_chars
            self.overlap = 0 if overlap is None else overlap
            self.overlap_all = False if overlap_all is None else overlap_all


class BaseChat:
    def __init__(
            self,
            name: str,
            desc: str,
            system_prompt_id: int,
            chat_model_id: int,
            doc_proc_cnf_id: int
    ):
        self.name = name
        self.desc = desc
        self.system_prompt_id = system_prompt_id
        self.chat_model_id = chat_model_id
        self.doc_proc_cnf_id = doc_proc_cnf_id


class ChatModel:
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
            api_key_credential: ApiKeyCredential = None
    ):
        self.name = name
        self.api_key_credential_id = api_key_credential_id
        self.temperature = temperature
        self.top_p = top_p
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.api_key_credential = api_key_credential
        self.stop_sequences = json.dumps(stop_sequences) if stop_sequences is not None else None

    @property
    def deserialized_stop_sequence(self) -> list[str] | None:
        """
        I need this method because of the db mapping 😥. Probably I did some bad designing.
        """
        return json.loads(self.stop_sequences) if self.stop_sequences is not None else None

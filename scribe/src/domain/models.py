import json

from src.enums import (
    Postprocessor,
    ChunkingStrategy,
    ChatModelName
)
from .base import Serializable


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
        self.postprocessors = postprocessors
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

        self.json_config = self.__form_json_config()

    def __form_json_config(self) -> str:
        """
        Forms json string out of passed attributes.
        """

        dict_ = {key: self.__dict__[key] for key in [
            'postprocessors',
            'chunking_strategy',
            'max_characters',
            'new_after_n_chars',
            'overlap',
            'overlap_all',
        ]}

        # extracting values from enums
        postproc = dict_.get('postprocessors')
        if postproc is not None:
            dict_['postprocessors'] = list(map(lambda item: item.value, postproc))

        strategy = dict_.get('chunking_strategy')
        if strategy is not None:
            dict_['chunking_strategy'] = strategy.value

        return json.dumps(dict_)


class BaseChat:
    def __init__(
            self,
            name: str,
            desc: str,
            system_prompt_id: int,
            api_key_credential_id: int,
            doc_proc_cnf_id: int
    ):
        self.name = name
        self.desc = desc
        self.system_prompt_id = system_prompt_id
        self.api_key_credential_id = api_key_credential_id
        self.doc_proc_cnf_id = doc_proc_cnf_id


class ChatModel(Serializable):

    def __init__(
            self,
            model_name: ChatModelName,
            api_key_credential_id: id,
            temperature: float | None,
            top_p: float | None,
            base_url: str | None,
            max_tokens: int | None,
            max_retries: int | None,
            stop_sequences: list[str] | None
    ):
        self.model_name = model_name.value
        self.api_key_credential_id = api_key_credential_id
        self.temperature = temperature
        self.top_p = top_p
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.stop_sequences = stop_sequences

    def __serialize(self) -> str:
        dict_ = {key: self.__dict__[key] for key in [
            'temperature',
            'top_p',
            'base_url',
            'max_tokens',
            'max_retries',
            'stop_sequences'
        ]}

        return json.dumps(dict_)

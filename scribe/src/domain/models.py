import copy
import json

from src.enums import (
    Postprocessors,
    ChunkingStrategy
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
            postprocessors: list[Postprocessors] | None,
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
        Forms json string out of attributes passed attributes.
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

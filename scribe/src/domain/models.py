import copy
import json

from src.enums import (
    UnstructuredPostprocessors,
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
            postprocessors: list[UnstructuredPostprocessors] | None,
            chunking_strategy: ChunkingStrategy | None,
            max_characters: int | None = 500,
            new_after_n_chars: int | None = 500,
            overlap: int | None = 0,
            overlap_all: bool | None = False

    ):
        self.name = name
        self.postprocessors = postprocessors
        self.chunking_strategy = chunking_strategy
        self.max_characters = max_characters
        self.new_after_n_chars = new_after_n_chars
        self.overlap = overlap
        self.overlap_all = overlap_all

    @property
    def json_config(self) -> str:
        dict_ = copy.copy(self.__dict__)
        dict_.pop('name')

        # extracting values from enums
        postproc = dict_.get('postprocessors')
        if postproc is not None:
            dict_['postprocessors'] = list(map(lambda item: item.value, postproc))

        strategy = dict_.get('chunking_strategy')
        if strategy is not None:
            dict_['chunking_strategy'] = strategy.value

        return json.dumps(dict_)

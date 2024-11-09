from enum import Enum


class Postprocessor(Enum):
    BYTES_STRING_TO_STRING = "bytes_string_to_string"
    CLEAN = "clean"
    CLEAN_BULLETS = "clean_bullets"
    CLEAN_DASHES = "clean_dashes"
    CLEAN_NON_ASCII_CHARS = "clean_non_ascii_chars"
    CLEAN_ORDERED_BULLETS = "clean_ordered_bullets"
    CLEAN_TRAILING_PUNCTUATION = "clean_trailing_punctuation"
    GROUP_BROKEN_PARAGRAPHS = "group_broken_paragraphs"
    REMOVE_PUNCTUATION = "remove_punctuation"
    REPLACE_UNICODE_QUOTES = "replace_unicode_quotes"


class ChunkingStrategy(Enum):
    BASIC = "basic"
    BY_TITLE = "by_title"


class ChatModelName(Enum):
    # open ai
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"

    # cohere
    COMMAND_R_PLUS = "command-r-plus"
    COMMAND = "command"

    # anthropic
    CLAUDE_3_5_SONNET_20241022 = "claude-3-5-sonnet-20241022"
    CLAUDE_3_5_HAIKU_20241022 = "claude-3-5-haiku-20241022"
    CLAUDE_3_OPUS_20240229 = "claude-3-opus-20240229"
    CLAUDE_3_SONNET_20240229 = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU_20240307 = "claude-3-haiku-20240307"


class ModelProvider(Enum):
    OPENAI = 'openai'
    COHERE = 'cohere'
    ANTHROPIC = 'anthropic'

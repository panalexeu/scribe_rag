import json
from enum import Enum
from typing import AsyncIterator
from src.adapters.msg_chunk import BaseMessageChunk


def JsonEnum(name: str, path: str):
    """
    Creates an Enum class based on the JSON data read from a file.
    """
    with open(path, 'r') as file:
        content = file.read()
        json_: dict = json.loads(content)

    return Enum(name, json_.get(name))


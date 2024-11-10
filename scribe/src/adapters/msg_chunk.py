from langchain_core.messages.ai import AIMessageChunk


class BaseMessageChunk:
    def __init__(self, content: str, **kwargs):
        self.content = content
        self.kwargs = kwargs


class LangChainMessageChunk(BaseMessageChunk, AIMessageChunk):
    pass


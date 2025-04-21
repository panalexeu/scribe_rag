from langchain_core.prompts import ChatPromptTemplate

from src.adapters.chroma_models import VectorChromaDocument


class ChatPromptTemplateBuilder:

    @staticmethod
    def build(
            system_prompt: str | None,
            docs: list[VectorChromaDocument] | None
    ) -> ChatPromptTemplate:
        context = None
        if docs is not None:
            context = ChatPromptTemplateBuilder.format_context(docs)

        return ChatPromptTemplate(
            messages=[
                ('system', 'You are a helpful AI-assistant.'),
                ('system', f'Context: {context}'),
                ('human', f'Preferences: {system_prompt}'),
                ('human', '{input}')
            ]
        )

    @staticmethod
    def format_context(docs: list[VectorChromaDocument]) -> str:
        """
        Removes '{', '}' in documents, to not ruin LangChain prompt template formatting.
        After that concatenates documents into one string separated with '\n'.
        """
        for doc in docs:
            doc.document = doc.document.replace('{', '').replace('}', '')

        return '\n'.join(list(map(lambda d: d.document, docs)))

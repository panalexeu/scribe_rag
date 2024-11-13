import io
from typing import Type

from langchain_unstructured.document_loaders import UnstructuredLoader

from src.domain.models import (
    DocProcessingConfig,
    VectorDocument
)


class UnsupportedFileFormatError(RuntimeError):
    supported_formats = ['.odt', '.md', 'text files']

    def __init__(self):
        super().__init__(
            f'Unsupported file formate provided. Currently supported are: {', '.join(self.supported_formats)}.'
        )


class LoadDocumentService:
    """
    Service that wraps around langchain_core.document_loaders.base.BaseLoader
    to load documents asynchronously.
    Works with loaders like:
        - langchain_unstructured.document_loaders.UnstructuredLoader;
    """

    def __init__(self, doc_loader: Type[UnstructuredLoader]):
        self.doc_loader = doc_loader

    # TODO make the loop truly async
    async def load_async(
            self,
            files: dict[str, bytes],
            doc_proc_cnf: DocProcessingConfig
    ) -> list[VectorDocument]:
        """
        :raises UnsupportedFileFormatError:
        """

        all_docs: list[VectorDocument] = []
        for filename, bytes_ in files.items():
            wrapped_bytes = io.BytesIO(bytes_)  # <-- BytesIO wrapping around bytes
            document_loader = self.doc_loader(
                file=wrapped_bytes,
                metadata_filename=filename,

            )

            try:
                docs = await document_loader.aload()
            except ImportError:
                raise UnsupportedFileFormatError

            all_docs.extend(
                list(
                    # mapping to VectorDocument
                    map(lambda d: VectorDocument(
                        page_content=d.page_content,
                        metadata=d.metadata
                    ), docs)
                )
            )

        return all_docs

    @staticmethod
    def build_config(doc_proc_cnf: DocProcessingConfig) -> dict:
        config = {}
        if doc_proc_cnf.chunking_strategy is not None:
            config['chunking_strategy'] = doc_proc_cnf.chunking_strategy

        if doc_proc_cnf.postprocessors is not None:
            ...

        return config

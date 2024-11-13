from hashlib import sha224

import io
from typing import Type
from langchain_core.document_loaders.base import BaseLoader, Document

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
    to load documents asynchronously. Assigns hash ids to document.
    Works with loaders like:
        - langchain_unstructured.document_loaders.UnstructuredLoader;
    """

    def __init__(self, doc_loader: Type[BaseLoader]):
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
                file=wrapped_bytes,  # type: ignore
                metadata_filename=filename  # type: ignore
            )

            try:
                docs = await document_loader.aload()
            except ImportError:
                raise UnsupportedFileFormatError

            all_docs.extend(
                list(
                    map(lambda d: VectorDocument(
                        d.page_content,
                        d.metadata
                    ), docs)
                )
            )

        return all_docs

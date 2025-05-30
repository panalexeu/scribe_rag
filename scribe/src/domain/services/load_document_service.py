import io
import re
import logging
from abc import ABC, abstractmethod
from typing import Type

import pymupdf
from langchain_unstructured.document_loaders import UnstructuredLoader
from unstructured.cleaners.core import (
    bytes_string_to_string,
    clean,
    clean_bullets,
    clean_dashes,
    clean_non_ascii_chars,
    clean_ordered_bullets,
    clean_trailing_punctuation,
    group_broken_paragraphs,
    remove_punctuation,
    replace_unicode_quotes
)
from horchunk.chunkers import WindowChunker, Chunk
from horchunk.splitters import SentenceSplitter
from chromadb.utils import embedding_functions
from langchain_core.documents.base import Document
from unstructured.partition.common import UnsupportedFileFormatError as UnstructuredUnsupportedFileFormatError

from src.enums import Postprocessor
from src.domain.models import (
    DocProcessingConfig,
    SemanticDocProcessingConfig,
    VectorDocument
)


class UnsupportedFileFormatError(RuntimeError):
    supported_formats = ['.odt', '.md', 'text files', '.pdf', '.html']

    def __init__(self):
        super().__init__(
            f'Unsupported file formate provided. Currently supported are: {', '.join(self.supported_formats)}.'
        )


class BaseLoadDocumentService(ABC):

    @abstractmethod
    async def load_async(
            self,
            *args,
            **kwargs
    ) -> list[VectorDocument]:
        pass


class LoadDocumentService(BaseLoadDocumentService):
    """
    Service that wraps around langchain_core.document_loaders.base.BaseLoader
    to load documents asynchronously.
    Works with loaders like:
        - langchain_unstructured.document_loaders.UnstructuredLoader;
    """

    def __init__(self, doc_loader: Type[UnstructuredLoader]):
        self.doc_loader = doc_loader

    # TODO make the loop truly documents
    async def load_async(
            self,
            files: dict[str, bytes] | None,
            urls: list[str] | None,
            doc_proc_cnf: DocProcessingConfig
    ) -> list[VectorDocument]:
        """
        Loads provided documents to list[VectorDocument] based on the provided DocProcessingConfig.

        :raises UnsupportedFileFormatError:
        """
        config = self.build_config(doc_proc_cnf)
        all_docs: list[VectorDocument] = []

        # handling url
        if urls is not None:
            for url in urls:
                document_loader = self.doc_loader(
                    web_url=url,
                    **config
                )

                docs = await document_loader.aload()

                all_docs.extend(
                    list(map(lambda d: self.map_doc(d), docs))
                )

        # handling files
        if files is not None:
            for filename, bytes_ in files.items():
                wrapped_bytes = io.BytesIO(bytes_)  # <-- BytesIO wrapping around bytes
                document_loader = self.doc_loader(
                    file=wrapped_bytes,
                    metadata_filename=filename,
                    **config
                )

                try:
                    docs = await document_loader.aload()
                except (ImportError, UnstructuredUnsupportedFileFormatError) as e:
                    logging.log(logging.ERROR, str(e))
                    raise UnsupportedFileFormatError

                all_docs.extend(
                    list(map(lambda d: self.map_doc(d), docs))
                )

        return all_docs

    @staticmethod
    def build_config(doc_proc_cnf: DocProcessingConfig) -> dict:
        config = {}
        if doc_proc_cnf.chunking_strategy is not None:
            config['chunking_strategy'] = doc_proc_cnf.chunking_strategy.value
            config['max_characters'] = doc_proc_cnf.max_characters
            config['new_after_n_chars'] = doc_proc_cnf.new_after_n_chars
            config['overlap'] = doc_proc_cnf.overlap
            config['overlap_all'] = doc_proc_cnf.overlap_all

        if doc_proc_cnf.deserialized_postprocessors is not None:
            cleaners = []
            for proc in doc_proc_cnf.deserialized_postprocessors:
                match proc:
                    case Postprocessor.BYTES_STRING_TO_STRING:
                        cleaners.append(bytes_string_to_string)
                    case Postprocessor.CLEAN:
                        cleaners.append(clean)
                    case Postprocessor.CLEAN_BULLETS:
                        cleaners.append(clean_bullets)
                    case Postprocessor.CLEAN_DASHES:
                        cleaners.append(clean_dashes)
                    case Postprocessor.CLEAN_NON_ASCII_CHARS:
                        cleaners.append(clean_non_ascii_chars)
                    case Postprocessor.CLEAN_ORDERED_BULLETS:
                        cleaners.append(clean_ordered_bullets)
                    case Postprocessor.CLEAN_TRAILING_PUNCTUATION:
                        cleaners.append(clean_trailing_punctuation)
                    case Postprocessor.GROUP_BROKEN_PARAGRAPHS:
                        cleaners.append(group_broken_paragraphs)
                    case Postprocessor.REMOVE_PUNCTUATION:
                        cleaners.append(remove_punctuation)
                    case Postprocessor.REPLACE_UNICODE_QUOTES:
                        cleaners.append(replace_unicode_quotes)

            unique_vals = set(cleaners)
            config['post_processors'] = list(unique_vals)

        return config

    @staticmethod
    def map_doc(doc: Document) -> VectorDocument:
        return VectorDocument(
            page_content=doc.page_content,
            metadata=doc.metadata
        )


class UnsupportedSemanticFileFormatError(RuntimeError):
    supported_formats = ['.pdf']

    def __init__(self):
        super().__init__(
            f'Unsupported file formate provided. Currently supported are: {', '.join(self.supported_formats)}.'
        )


class SemanticLoadDocumentService(BaseLoadDocumentService):

    async def load_async(
            self,
            files: dict[str, bytes],
            doc_proc_cnf: SemanticDocProcessingConfig,
            embedding_function: embedding_functions.EmbeddingFunction
    ) -> list[VectorDocument]:

        chunker = WindowChunker(
            embedding_function,
            thresh=doc_proc_cnf.thresh,
            max_chunk_size=doc_proc_cnf.max_chunk_size
        )

        all_docs = []
        for filename, bytes_ in files.items():
            # checking extension
            ext = filename.split('.')[-1]
            self.check_file_ext(ext)

            # extracting content
            doc = pymupdf.open(filetype=ext, stream=bytes_)
            full_text = " ".join(doc.load_page(i).get_text() for i in range(doc.page_count))
            full_text = self.normalize_pdf(full_text)

            # chunking
            splits = SentenceSplitter(full_text).__call__()
            chunks = chunker(splits)

            # mapping chunks to VectorDocument
            vector_docs = self.map_chunks(chunks, filename)
            all_docs.extend(vector_docs)

        return all_docs

    @staticmethod
    def check_file_ext(ext: str) -> None:
        if ext not in ['pdf']:
            raise UnsupportedSemanticFileFormatError()

    @staticmethod
    def normalize_pdf(text: str) -> str:
        return re.sub(r'(?<!\n)\n(?!\n)', ' ', text).strip()


    @staticmethod
    def map_chunks(chunks: list[Chunk], filename: str) -> list[VectorDocument]:
        documents = []
        for chunk in chunks:
            documents.append(VectorDocument(
                page_content=chunk.join(),
                metadata={
                    'size': chunk.size,
                    'chars': chunk.chars,
                    'tokens': chunk.tokens,
                    'filename': filename,
                }
            ))

        return documents

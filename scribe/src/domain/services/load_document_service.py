import io
from typing import Type

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
from src.enums import Postprocessor
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
        Loads provided documents to list[VectorDocument] based on the provided DocProcessingConfig.

        :raises UnsupportedFileFormatError:
        """
        config = self.build_config(doc_proc_cnf)

        all_docs: list[VectorDocument] = []
        for filename, bytes_ in files.items():
            wrapped_bytes = io.BytesIO(bytes_)  # <-- BytesIO wrapping around bytes
            document_loader = self.doc_loader(
                file=wrapped_bytes,
                metadata_filename=filename,
                **config
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

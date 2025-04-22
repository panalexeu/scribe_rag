"""
Primitive mappings of chroma objects, retrieved from the db, to serializable python objects.
"""
import numpy
from chromadb.api import Collection
from typing import Optional


class VectorChromaDocument:
    """View of a document from Chroma."""

    def __init__(
            self,
            id_: str,
            document: str,
            metadata: dict[str, list | str | int | float],
            embedding: numpy.ndarray,
            distance: Optional[float] = None
    ):
        self.id_ = id_[:16] + '...'
        self.document = document
        self.metadata = self._filter_metadata(metadata)
        self.embedding: str = self._embedding_repr(embedding)
        self.distance = round(distance, 4) if distance else None

    @staticmethod
    def _embedding_repr(embedding: numpy.ndarray) -> str:
        return f'[{embedding[0]} ... {embedding[-1]}] {len(embedding)} items'

    @staticmethod
    def _filter_metadata(metadata: dict) -> dict:
        """Removes from final vector document view specified fields."""
        filter_keys = [
            'category',
            'element_id',
            'orig_elements'
        ]

        for key in filter_keys:
            metadata.pop(key)

        return metadata

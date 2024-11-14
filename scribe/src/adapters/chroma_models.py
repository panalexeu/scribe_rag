"""
Primitive mappings of chroma objects, retrieved from the db, to serializable python objects.
"""
import numpy
from chromadb.api import Collection
from typing import Optional


class VectorCollection:
    """
    Maps ChromaDB Collection to VectorCollection
    """

    def __init__(
            self,
            collection: Collection
    ):
        self.name: str = collection.name
        self.embedding_function: str = collection._embedding_function.__repr__()
        self.metadata: dict[str, str] | None = collection.metadata


class VectorChromaDocument:
    def __init__(
            self,
            id_: str,
            document: str,
            metadata: dict[str, list | str | int | float],
            embedding: numpy.ndarray,
            distance: Optional[float] = None
    ):
        self.id_ = id_
        self.document = document
        self.metadata = metadata
        self.embedding: str = self.embedding_repr(embedding)
        self.distance = distance

    @staticmethod
    def embedding_repr(embedding: numpy.ndarray) -> str:
        return f'[{embedding[0]} {embedding[1]} {embedding[2]} ... {embedding[-3]} {embedding[-2]} {embedding[-1]}] {len(embedding)} items'

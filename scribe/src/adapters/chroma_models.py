"""
Primitive mappings of chroma objects, retrieved from the db, to serializable python objects.
"""

from chromadb.api import Collection


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

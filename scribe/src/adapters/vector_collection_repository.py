from typing import Optional, Callable, Sequence
from abc import ABC

from chromadb.api.models import Collection
from chromadb import AsyncClientAPI


class AsyncAbstractVectorCollectionRepository[T](ABC):

    async def add(self, name: str, embedding_function: Optional[Callable] = None, **kwargs) -> T:
        pass

    async def read(self, name: str, embedding_function: Optional[Callable] = None) -> T:
        pass

    async def read_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[T]:
        pass

    async def update(self, **kwargs) -> T:
        pass

    async def delete(self, name: str) -> None:
        pass

    async def count(self) -> int:
        pass


class CollectionNameError(LookupError):
    def __init__(self, name: str):
        super().__init__(f"Collection with the name: '{name}' already exists, or the provided name is invalid.")


class CollectionNotFoundError(LookupError):
    def __init__(self, name: str):
        super().__init__(f"Collection with the name: '{name}' is not found:")


class AsyncChromaDBVectorCollectionRepository:

    def __init__(self, client: AsyncClientAPI):
        self.client = client

    async def add(self, name: str, embedding_function: Optional[Callable] = None, **kwargs) -> Collection:
        """
        :param name: Name of a collection to create.
        :param embedding_function: If no embedding_function supplied - default is used.
        """
        try:
            return await self.client.create_collection(name=name, embedding_function=embedding_function, **kwargs)
        except Exception:
            raise CollectionNameError(name)

    async def read(self, name: str, embedding_function: Optional[Callable] = None) -> Collection:
        """
        :param name: name of a previously created collection
        :param embedding_function: from ChromaDB docs: "If you later wish to get_collection, you MUST do so with the
        embedding function you supplied while creating the collection". If no embedding_function supplied - default is
        used.
        """
        try:
            return await self.client.get_collection(name=name, embedding_function=embedding_function)
        except ValueError:
            raise CollectionNotFoundError(name)

    async def read_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[Collection]:
        return await self.client.list_collections(limit, offset)

    async def update(self, **kwargs) -> Collection:
        raise NotImplementedError

    async def delete(self, name: str) -> None:
        try:
            return await self.client.delete_collection(name)
        except ValueError:
            raise CollectionNotFoundError(name)

    async def count(self) -> int:
        return await self.client.count_collections()

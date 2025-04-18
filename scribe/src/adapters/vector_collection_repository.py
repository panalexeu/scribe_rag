from typing import Optional, Callable, Sequence
from abc import ABC

from chromadb.api.models import AsyncCollection
from chromadb import AsyncClientAPI
from chromadb.errors import InvalidCollectionException, InvalidArgumentError
from chromadb.api.types import GetResult

from src.adapters.chroma_models import VectorChromaDocument
from src.domain.models import VectorDocument


class AbstractAsyncVectorCollectionRepository[T](ABC):

    async def add(self, name: str, embedding_function: Optional[Callable] = None, **kwargs) -> T:
        pass

    async def read(self, name: str, embedding_function: Optional[Callable] = None, **kwargs) -> T:
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
        super().__init__(f"Collection with the name: '{name}' is not found.")


class AsyncChromaVectorCollectionRepository(AbstractAsyncVectorCollectionRepository[AsyncCollection]):

    def __init__(self, client: AsyncClientAPI):
        self.client = client

    async def add(self, name: str, embedding_function: Optional[Callable] = None, **kwargs) -> AsyncCollection:
        """
        :param name: Name of a collection to create.
        :param embedding_function: If no embedding_function supplied - default is used.
        :raises CollectionNamerError:
        """
        try:
            return await self.client.create_collection(name=name, embedding_function=embedding_function, **kwargs)
        except Exception:
            raise CollectionNameError(name)

    async def read(self, name: str, embedding_function: Optional[Callable] = None, **kwargs) -> AsyncCollection:
        """
        :param name: name of a previously created collection
        :param embedding_function: from ChromaDB docs: "If you later wish to get_collection, you MUST do so with the
        embedding function you supplied while creating the collection". If no embedding_function supplied - default is
        used.
        :raises CollectionNamerError:
        """
        try:
            return await self.client.get_collection(name=name)
        except InvalidCollectionException:
            raise CollectionNotFoundError(name)

    async def read_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> Sequence[AsyncCollection]:
        return await self.client.list_collections(limit, offset)

    async def update(self, **kwargs) -> AsyncCollection:
        raise NotImplementedError

    async def delete(self, name: str) -> None:
        try:
            return await self.client.delete_collection(name)
        except InvalidArgumentError:
            raise CollectionNotFoundError(name)

    async def count(self) -> int:
        return await self.client.count_collections()


class AbstractAsyncDocumentRepository(ABC):
    async def add(self, docs):
        pass

    async def read(self):
        pass

    async def read_all(self, limit: int | None, offset: int | None):
        pass

    async def update(self):
        pass

    async def delete(self, doc_name):
        pass

    async def count(self):
        pass

    async def peek(self):
        pass

    async def query(self, query_string, doc_names, n_results):
        pass

    async def list_documents(self):
        pass


class AsyncChromaDocumentRepository(AbstractAsyncDocumentRepository):
    def __init__(self, async_collection: AsyncCollection):
        self.async_collection = async_collection

    async def add(self, docs: list[VectorDocument]) -> None:
        for doc in docs:
            await self.async_collection.add(
                ids=doc.id_,
                metadatas=doc.metadata,
                documents=doc.page_content
            )

        return None

    async def read(self):
        raise NotImplementedError

    async def read_all(self, limit: int | None, offset: int | None) -> list[VectorChromaDocument]:
        res = await self.async_collection.get(
            limit=limit,
            offset=offset,
            include=["metadatas", "documents", "embeddings"]
        )

        return self.map_get_result(res)

    async def update(self):
        raise NotImplementedError

    async def delete(self, doc_name: str) -> None:
        return await self.async_collection.delete(
            where={
                '$or': [
                    {
                        'filename': {
                            '$eq': doc_name
                        }
                    },
                    {
                        'url': {
                            '$eq': doc_name
                        }
                    }
                ]

            }
        )

    async def count(self):
        return await self.async_collection.count()

    async def peek(self) -> list[VectorChromaDocument]:
        res = await self.async_collection.peek(limit=3)
        return self.map_get_result(res)

    async def query(
            self,
            query_string: str,
            doc_names: Optional[list[str]] = None,
            n_results: Optional[int] = None,
    ) -> list[VectorChromaDocument]:
        if n_results is None:
            n_results = 1

        search_dict = None
        if doc_names is not None:
            search_dict = {
                '$or': [
                    {
                        'filename': {
                            '$in': doc_names
                        }
                    },
                    {
                        'url': {
                            '$in': doc_names
                        }
                    }
                ]
            }

        res = await self.async_collection.query(
            query_texts=query_string,
            include=['metadatas', 'embeddings', 'documents', 'distances'],
            n_results=n_results,
            where=search_dict
        )

        return self.map_query_get_result(res)

    async def list_documents(self) -> list[str]:
        res = await self.async_collection.get()

        doc_names = set()
        for item in res['metadatas']:
            filename = item.get('filename')
            url = item.get('url')

            if filename:
                doc_names.add(filename)
            elif url:
                doc_names.add(url)

        return list(doc_names)

    @staticmethod
    def map_get_result(res: GetResult) -> list[VectorChromaDocument]:
        mapped_res: list[VectorChromaDocument] = []
        for id_, document, metadata, embedding in zip(
                res['ids'],
                res['documents'],
                res['metadatas'],
                res['embeddings'],
        ):
            mapped_res.append(
                VectorChromaDocument(
                    id_=id_,
                    document=document,
                    metadata=metadata,
                    embedding=embedding,
                )
            )

        return mapped_res

    @staticmethod
    def map_query_get_result(res: GetResult) -> list[VectorChromaDocument]:
        mapped_res: list[VectorChromaDocument] = []
        for id_, document, metadata, embedding, distance in zip(
                *res['ids'],
                *res['documents'],
                *res['metadatas'],
                *res['embeddings'],
                *res['distances']  # type: ignore
        ):
            mapped_res.append(
                VectorChromaDocument(
                    id_=id_,
                    document=document,
                    metadata=metadata,
                    embedding=embedding,
                    distance=distance
                )
            )

        return mapped_res

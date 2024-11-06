import os

import pytest
from langchain_unstructured.document_loaders import UnstructuredLoader

from src.domain.services import LoadDocumentService


@pytest.fixture(scope='session')
def doc_loader():
    return LoadDocumentService(UnstructuredLoader)


@pytest.fixture(scope='session')
def fake_files():
    file_content = {}
    with os.scandir('./tests/unit/test_files') as scan:
        for entry in scan:
            with open(entry, 'rb') as file:
                file_content[entry.name] = file.read()

    return file_content


@pytest.mark.asyncio
async def test_unstructured_doc_loader_successfully_loads_one_file(doc_loader, fake_files):
    filename = 'lorem-ipsum.txt'
    res = await doc_loader.load_async({filename: fake_files.get(filename)})
    print(res)

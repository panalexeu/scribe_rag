import os

import pytest
from langchain_unstructured.document_loaders import UnstructuredLoader
from langchain_core.documents.base import Document

from src.domain.services import LoadDocumentService


@pytest.fixture(scope='session')
def doc_loader():
    return LoadDocumentService(UnstructuredLoader)


@pytest.fixture(scope='session')
def fake_files():
    path = './tests/async/test_files'
    file_content = {}
    with os.scandir(path) as scan:
        for entry in scan:
            with open(entry, 'rb') as file:
                file_content[entry.name] = file.read()

    return file_content


@pytest.mark.asyncio
async def test_unstructured_doc_loader_successfully_loads_one_file(doc_loader, fake_files):
    filename = 'lorem-ipsum.txt'
    res = await doc_loader.load_async({filename: fake_files.get(filename)})
    doc = res[0]

    assert isinstance(doc, Document)
    assert doc.__dict__.get('metadata')
    assert doc.__dict__.get('page_content')


@pytest.mark.asyncio
async def test_unstructured_doc_loader_successfully_loads_multiple_files(doc_loader, fake_files):
    res = await doc_loader.load_async(fake_files)

    for doc in res:
        assert isinstance(doc, Document)

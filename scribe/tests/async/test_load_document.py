import os

import pytest
from langchain_unstructured.document_loaders import UnstructuredLoader
from langchain_core.documents.base import Document

from src.domain.services import LoadDocumentService, UnsupportedFileFormatError


@pytest.fixture(scope='session')
def doc_loader():
    return LoadDocumentService(UnstructuredLoader)


@pytest.fixture(scope='session')
def fake_files():
    path = './tests/async/test_files'
    file_content = {}
    with os.scandir(path) as scan:
        for entry in scan:
            if entry.name.split('.')[-1] != 'pdf':
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


@pytest.mark.asyncio
async def test_unsupported_type_error_is_raised_in_doc_loader_service_if_invalid_format_is_provided(doc_loader):
    path = './tests/async/test_files'
    name = 'lorem-ipsum.pdf'

    file_content = {}
    with open(os.path.join(path, name), 'rb') as file:
        file_content[name] = file.read()

    with pytest.raises(UnsupportedFileFormatError):
        await doc_loader.load_async(file_content)

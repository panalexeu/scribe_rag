import os

import pytest
from langchain_unstructured.document_loaders import UnstructuredLoader
from langchain_core.documents.base import Document

from src.domain.services.load_document_service import LoadDocumentService, UnsupportedFileFormatError
from src.domain.models import DocProcessingConfig, VectorDocument


@pytest.fixture(scope='session')
def doc_loader():
    return LoadDocumentService(UnstructuredLoader)


@pytest.fixture(scope='session')
def fake_files():
    path = './tests/test_files'
    file_content = {}
    with os.scandir(path) as scan:
        for entry in scan:
            if entry.name.split('.')[-1] != 'odp':
                with open(entry, 'rb') as file:
                    file_content[entry.name] = file.read()

    return file_content


@pytest.fixture(scope='session')
def doc_proc_cnf():
    return DocProcessingConfig(
        'fake',
        None, None, None, None, None, None
    )


@pytest.mark.asyncio
async def test_unstructured_doc_loader_successfully_loads_one_file(doc_loader, fake_files, doc_proc_cnf):
    filename = 'lorem-ipsum.txt'
    res = await doc_loader.load_async({filename: fake_files.get(filename)}, None, doc_proc_cnf)
    doc = res[0]

    assert isinstance(doc, VectorDocument)
    assert doc.__dict__.get('metadata')
    assert doc.__dict__.get('page_content')


@pytest.mark.asyncio
async def test_unstructured_doc_loader_successfully_loads_multiple_files(doc_loader, fake_files, doc_proc_cnf):
    res = await doc_loader.load_async(fake_files, None, doc_proc_cnf)

    for doc in res:
        assert isinstance(doc, VectorDocument)


@pytest.mark.asyncio
async def test_unsupported_type_error_is_raised_in_doc_loader_service_if_invalid_format_is_provided(
        doc_loader,
        doc_proc_cnf
):
    path = './tests/test_files'
    name = 'lorem-ipsum.odp'

    file_content = {}
    with open(os.path.join(path, name), 'rb') as file:
        file_content[name] = file.read()

    with pytest.raises(UnsupportedFileFormatError):
        await doc_loader.load_async(file_content, None, doc_proc_cnf)

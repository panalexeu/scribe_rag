import numpy
import pytest

from src.adapters.chroma_models import VectorChromaDocument


@pytest.fixture
def fake_doc():
    metadata = {
        "category": "fake",
        "element_id": "fake",
        "filename": "fake",
        "filetype": "fake",
        "languages": "fake",
        "orig_elements": "fake",
        "page_number": 1
    }

    return VectorChromaDocument(
        'fake-id',
        'fake-doc',
        metadata=metadata,
        embedding=numpy.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]),
        distance=0.23
    )


def test_vector_chroma_document_forms_embedding_repr(fake_doc):
    assert isinstance(fake_doc.embedding, str)
    assert fake_doc.embedding == '[0.1 ... 0.6] 6 items'


def test_vector_chroma_document_filters_metadata_fields(fake_doc):
    filter_fields = ['category', 'element_id', 'orig_elements']

    assert sum([
        key not in filter_fields
        for key in fake_doc.metadata.keys()
    ]) == len(fake_doc.metadata.keys())  # sum of True's should equal to the amount of metadata fields

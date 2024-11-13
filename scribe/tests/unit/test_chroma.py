import numpy

from src.adapters.chroma_models import VectorChromaDocument


def test_vector_chroma_document_forms_embedding_repr():
    doc = VectorChromaDocument(
        'fake-id',
        'fake-doc',
        metadata={'fake': 'data'},
        embedding=numpy.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    )

    assert isinstance(doc.embedding, str)
    assert doc.embedding == '[0.1 0.2 0.3 ... 0.4 0.5 0.6] 6 items'

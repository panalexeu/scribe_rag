from .conftest import client, fake_chdb


def test_vec_doc_add(client, fake_chdb):
    # vec-doc depends on embed-model, doc-proc-cnf and vec-col
    client.post(
        url='/embed-model/',
        json={
            "name": "all-MiniLM-L6-v2",
            "api_key_credential_id": 0
        }
    )
    client.post(
        '/vec-col/',
        json={
            "name": "string",
            "embedding_model_id": 1,
            "distance_func": "l2"
        }
    )
    client.post(
        '/doc-proc-cnf/',
        json={
            "name": "string"
        }
    )

    # sending url in the multipart/form-data request
    res = client.post(
        url='/vec-doc/string',
        data={
            'doc_processing_cnf_id': 1,
            'urls': ['https://en.wikipedia.org/wiki/Assembly']
        },
        files=dict()
    )

    assert res.status_code == 201


def test_vec_doc_list_docs(client, fake_chdb):
    res = client.get(
        url='/vec-doc/string/docs'
    )

    assert res.status_code == 200
    assert 'https://en.wikipedia.org/wiki/Assembly' == res.json()[0]


def test_vec_doc_read_all(client, fake_chdb):
    res = client.get(
        url='/vec-doc/string'
    )

    assert res.status_code == 200
    assert len(res.json()) > 0


def test_vec_doc_peek(client, fake_chdb):
    res = client.get(
        url='/vec-doc/string/peek'
    )

    assert res.status_code == 200
    assert len(res.json()) == 3


def test_vec_doc_query(client, fake_chdb):
    res = client.post(
        url='/vec-doc/string/query',
        json={
            "query_string": "string",
            'doc_names': None,
            "n_results": 1
        }
    )

    assert res.status_code == 200
    assert len(res.json()) == 1


def test_vec_doc_delete(client, fake_chdb):
    res = client.request(
        method='DELETE',
        url='/vec-doc/string',
        json={
            'doc_name': 'https://en.wikipedia.org/wiki/Assembly'
        }
    )

    assert res.status_code == 204


def test_vec_doc_count(client, fake_chdb):
    res = client.get(
        url='/vec-doc/string/count',
    )

    assert res.status_code == 200
    assert res.json() == 0

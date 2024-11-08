from .conftest import client


def test_doc_proc_cnf_creates(client):
    res = client.post(
        '/doc-proc-cnf/',
        json={
            "name": "string",
            "postprocessors": [
                "bytes_string_to_string"
            ],
            "chunking_strategy": "basic",
            "max_characters": 0,
            "new_after_n_chars": 0,
            "overlap": 0,
            "overlap_all": True
        }
    )

    assert res.status_code == 201


def test_doc_proc_cnf_reads(client):
    res = client.get(
        '/doc-proc-cnf/1'
    )

    assert res.status_code == 200


def test_doc_proc_cnf_reads_all(client):
    res = client.get(
        '/doc-proc-cnf/'
    )

    assert len(res.json()) == 1
    assert res.status_code == 200


def test_doc_proc_cnf_updates(client):
    res = client.put(
        '/doc-proc-cnf/1',
        json={

            "name": "string",
            "postprocessors": "string",
            "chunking_strategy": "basic",
            "max_characters": 0,
            "new_after_n_chars": 0,
            "overlap": 0,
            "overlap_all": True
        }
    )

    assert res.status_code == 200
    assert res.json()['postprocessors'] == 'string'


def test_doc_proc_cnf_deletes(client):
    res = client.delete(
        '/doc-proc-cnf/1'
    )

    assert res.status_code == 204


def test_doc_proc_cnf_counts(client):
    res = client.get(
        '/doc-proc-cnf/count'
    )

    assert res.json() == 0
    assert res.status_code == 200

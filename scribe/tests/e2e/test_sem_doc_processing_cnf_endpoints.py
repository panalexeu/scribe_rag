from .conftest import client


def test_sem_doc_proc_cnf_creates(client):
    res = client.post(
        '/sem-doc-proc-cnf/',
        json={
            'thresh': 0.5,
            'max_chunk_size': 1
        }
    )

    assert res.status_code == 201


def test_sem_doc_proc_cnf_reads(client):
    res = client.get(
        '/sem-doc-proc-cnf/1'
    )

    assert res.status_code == 200


def test_sem_doc_proc_cnf_reads_all(client):
    res = client.get(
        '/sem-doc-proc-cnf/'
    )

    assert len(res.json()) == 1
    assert res.status_code == 200


def test_sem_doc_proc_cnf_updates(client):
    res = client.put(
        '/sem-doc-proc-cnf/1',
        json={
            'thresh': 0.7,
            'max_chunk_size': 10
        }
    )

    assert res.status_code == 200
    assert res.json()['thresh'] == 0.7
    assert res.json()['max_chunk_size'] == 10


def test_sem_doc_proc_cnf_deletes(client):
    res = client.delete(
        '/sem-doc-proc-cnf/1'
    )

    assert res.status_code == 204


def test_sem_doc_proc_cnf_counts(client):
    res = client.get(
        '/sem-doc-proc-cnf/count'
    )

    assert res.json() == 0
    assert res.status_code == 200

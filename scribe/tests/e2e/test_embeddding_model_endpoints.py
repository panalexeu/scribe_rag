from .conftest import client


def test_embed_model_adds(client):
    res = client.post(
        url='/embed-model/',
        json={
            "name": "all-MiniLM-L6-v2",
            "api_key_credential_id": 0
        }
    )

    assert res.status_code == 201


def test_embed_model_reads(client):
    res = client.get(
        url='/embed-model/1'
    )

    assert res.status_code == 200


def test_embed_model_reads_all(client):
    res = client.get(
        url='/embed-model/'
    )

    assert len(res.json()) == 1
    assert res.status_code == 200


def test_embed_model_updates(client):
    res = client.put(
        url='/embed-model/1',
        json={
            'name': 'all-MiniLM-L6-v2',
            'api_key_credential_id': 1
        }
    )

    assert res.status_code == 200
    assert res.json()['api_key_credential_id'] == 1


def test_embed_model_deletes(client):
    res = client.delete(
        url='/embed-model/1'
    )

    assert res.status_code == 204


def test_embed_model_counts(client):
    res = client.get(
        url='/embed-model/count'
    )

    assert res.status_code == 200
    assert res.json() == 0

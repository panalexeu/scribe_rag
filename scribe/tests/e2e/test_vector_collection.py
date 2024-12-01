from .conftest import client


def test_vec_col_add(client):
    # vec-col depends on embed-model
    client.post(
        url='/embed-model/',
        json={
            "name": "all-MiniLM-L6-v2",
            "api_key_credential_id": 0
        }
    )

    res = client.post(
        '/vec-col/',
        json={
            "name": "string",
            "embedding_model_id": 1,
            "distance_func": "l2"
        }
    )

    assert res.status_code == 201


def test_vec_col_read(client):
    res = client.get(
        '/vec-col/string'
    )

    assert res.status_code == 200


def test_vec_col_read_all(client):
    res = client.get(
        '/vec-col/'
    )

    assert len(res.json()) == 1
    assert res.status_code == 200


def test_vec_col_deletes(client):
    res = client.delete(
        '/vec-col/string'
    )

    assert res.status_code == 204


def test_vec_col_counts(client):
    res = client.get(
        '/vec-col/count'
    )

    assert res.status_code == 200
    assert res.json() == 0

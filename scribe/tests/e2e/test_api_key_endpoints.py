"""
Tests in this module must be executed sequentially from start to finish.
"""
from .conftest import client


def test_api_key_post(client):
    res = client.post(
        url='/api-key/',
        json={'name': 'fake-ai', 'api_key': '12345'}
    )
    json = res.json()

    assert json.get('id') == 1
    assert json.get('name') == 'fake-ai'
    assert json.get('datetime') is not None
    assert json.get('api_key') != '12345'
    assert res.status_code == 201


def test_api_key_read(client):
    res = client.get(url='/api-key/1')
    json = res.json()

    assert json.get('id') == 1
    assert json.get('name') == 'fake-ai'
    assert json.get('datetime') is not None
    assert json.get('api_key') != '12345'
    assert res.status_code == 200


def test_api_key_read_all(client):
    res = client.get(
        url='/api-key/',
        params={'limit': 1, 'offset': 0}
    )
    json = res.json()
    api_key = json[0]

    assert len(json) == 1
    assert api_key.get('id') == 1
    assert api_key.get('name') == 'fake-ai'
    assert api_key.get('datetime') is not None
    assert api_key.get('api_key') != '12345'
    assert res.status_code == 200


def test_api_key_put(client):
    res = client.put(
        url='/api-key/1',
        json={'name': 'cohere'}
    )
    json = res.json()

    assert json.get('id') == 1
    assert json.get('name') == 'cohere'
    assert json.get('datetime') is not None
    assert json.get('api_key') != '12345'
    assert res.status_code == 200


def test_api_key_delete(client):
    res = client.delete(url='/api-key/1')

    assert res.status_code == 204


def test_api_key_counts(client):
    res = client.get('/api-key/count')

    assert res.json() == 0
    assert res.status_code == 200

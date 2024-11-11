from .conftest import client


def test_chat_model_add(client):
    res = client.post(
        url='/chat-model/',
        json={
            "name": "gpt-4o-mini",
            "api_key_credential_id": 0,
            "temperature": 0,
            "top_p": 0,
            "base_url": "string",
            "max_tokens": 0,
            "max_retries": 0,
            "stop_sequences": [
                "string"
            ]
        }
    )

    assert res.status_code == 201


def test_chat_model_read(client):
    res = client.get(
        url='/chat-model/1',
    )

    assert res.status_code == 200


def test_chat_model_read_all(client):
    res = client.get(
        url='/chat-model/',
        params={'limit': 1, 'offset': 0}
    )

    assert len(res.json()) == 1
    assert res.status_code == 200


def test_chat_model_updates(client):
    res = client.put(
        url='/chat-model/1',
        json={
            'name': 'command'
        }
    )

    assert res.json()['name'] == 'command'
    assert res.status_code == 200


def test_chat_model_deletes(client):
    res = client.delete(
        url='/chat-model/1'
    )

    assert res.status_code == 204


def test_chat_model_counts(client):
    res = client.get(
        url='/chat-model/count'
    )

    assert res.json() == 0
    assert res.status_code == 200

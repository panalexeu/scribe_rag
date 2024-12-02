from .conftest import client


def test_base_chat_adds(client):
    # chat-model depends on api-key
    client.post(
        url='/api-key/',
        json={
            'name': 'test',
            'key': 'fake'
        }
    )
    # base-chat depends on chat-model
    client.post(
        url='/chat-model/',
        json={
            "name": "gpt-4o-mini",
            "api_key_credential_id": 1,
        }
    )

    res = client.post(
        '/base-chat/',
        json={
            "name": "string",
            "desc": "string",
            "chat_model_id": 1
        }
    )

    assert res.status_code == 201


def test_base_chat_reads(client):
    res = client.get(
        '/base-chat/1'
    )

    assert res.status_code == 200


def test_base_chat_reads_all(client):
    res = client.get(
        '/base-chat/'
    )

    assert len(res.json()) == 1
    assert res.status_code == 200


def test_base_chat_updates(client):
    res = client.put(
        '/base-chat/1',
        json={
            "name": "string",
            "desc": "stringer",
            "chat_model_id": 1
        }
    )

    assert res.json()['desc'] == 'stringer'
    assert res.status_code == 200


def test_base_chat_deletes(client):
    res = client.delete(
        '/base-chat/1'
    )

    assert res.status_code == 204


def test_base_chat_counts(client):
    res = client.get(
        '/base-chat/count'
    )

    assert res.json() == 0
    assert res.status_code == 200

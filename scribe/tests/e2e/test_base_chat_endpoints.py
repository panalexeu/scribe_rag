from .conftest import client


def test_base_chat_adds(client):
    res = client.post(
        '/base-chat/',
        json={
            "name": "string",
            "desc": "string",
            "system_prompt_id": 0,
            "chat_model_id": 0,
            "chat_model_api_key_id": 0,
            "doc_proc_cnf_id": 0
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
            "desc": "string",
            "system_prompt_id": 0,
            "chat_model_id": 1,
            "chat_model_api_key_id": 0,
            "doc_proc_cnf_id": 0
        }
    )

    assert res.json()['chat_model_id'] == 1
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

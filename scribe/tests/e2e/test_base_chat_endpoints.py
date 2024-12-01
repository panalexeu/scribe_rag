from .conftest import client


def test_base_chat_adds(client):
    # setup
    res = client.post(
        '/base-chat/',
        json={
            "name": "string",
            "desc": "string",
            "chat_model_id": 1,
            "doc_proc_cnf_id": None,
            "system_prompt_id": None,
        }
    )

    print(res)

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

"""
Tests in this module must be executed sequentially from start to finish.
"""
import pytest

from .conftest import client


@pytest.fixture
def fake_data():
    return 'fake-name', 'fake-content'


def test_sys_prompt_post(client, fake_data):
    name, content = fake_data
    res = client.post(
        url='/sys-prompt/',
        json={'name': name, 'content': content}
    )
    json = res.json()

    assert json['id'] == 1
    assert json['name'] == name
    assert json['content'] == content
    assert json['datetime'] is not None
    assert res.status_code == 201


def test_sys_prompt_read(client, fake_data):
    name, content = fake_data
    res = client.get('/sys-prompt/1')
    json = res.json()

    assert json['id'] == 1
    assert json['name'] == name
    assert json['content'] == content
    assert json['datetime'] is not None
    assert res.status_code == 200


def test_sys_prompt_read_all(client, fake_data):
    name, content = fake_data
    res = client.get(
        url='/sys-prompt/',
        params={'limit': 1, 'offset': 0}
    )
    json = res.json()
    prompt = json[0]

    assert len(json) == 1
    assert prompt['id'] == 1
    assert prompt['name'] == name
    assert prompt['content'] == content
    assert prompt['datetime'] is not None
    assert res.status_code == 200


def test_sys_prompt_put(client):
    name, content = 'new-fake-name', 'new-fake-content'
    res = client.put(
        url='/sys-prompt/1',
        json={'name': name, 'content': content}
    )
    json = res.json()

    assert json['id'] == 1
    assert json['name'] == name
    assert json['content'] == content
    assert json['datetime'] is not None
    assert res.status_code == 200


def test_sys_prompt_delete(client):
    res = client.delete('/sys-prompt/1')

    assert res.status_code == 204

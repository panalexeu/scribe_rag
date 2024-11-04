import pytest
from fastapi.testclient import TestClient

from src.api.app import app
from src.bootstrap import bootstrap


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    bootstrap()  # <-- bootstrap here, because TestClient doesn't capture defined lifespan
    yield client


def test_root(client):
    res = client.get('/')
    json = res.json()

    assert json.get('detail') == 'beep boop beep'


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

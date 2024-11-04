from .conftest import client


def test_root(client):
    res = client.get('/')
    json = res.json()

    assert json.get('detail') == 'beep boop beep'

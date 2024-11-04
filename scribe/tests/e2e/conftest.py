import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import clear_mappers

from src.api.app import app
from src.bootstrap import bootstrap


@pytest.fixture(scope='module')
def client():
    client = TestClient(app)
    bootstrap()  # <-- bootstrap here, because TestClient doesn't capture defined lifespan
    yield client
    clear_mappers()

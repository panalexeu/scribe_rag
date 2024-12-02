import os
import sys
import subprocess
import shutil
import time
from requests import ConnectionError, get

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import clear_mappers

from src.api.app import app
from src.bootstrap import bootstrap


@pytest.fixture(scope='module')
def client():
    # checking for the SCRIBE_DB configuration to be 'dev'
    if status := os.getenv('SCRIBE_DB'):
        if status != 'dev':
            raise Exception('Change or provide the env SCRIBE_DB status as \'dev\'')

    client = TestClient(app)
    bootstrap()  # <-- bootstrap here, because TestClient doesn't capture defined lifespan
    yield client
    clear_mappers()


@pytest.fixture(scope='module')
def fake_chdb():
    print('Starting fake ChromaDB...')
    process = subprocess.Popen([
        "chroma", "run",
        "--path", "./chroma_fake",
        "--port", "8001"
    ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    pid = process.pid
    print(f'Fake ChromaDB started with the PID: {pid}')

    # checking does the fake chdb started before yielding it
    while True:
        if chdb_started():
            break
        else:
            time.sleep(0.5)

    yield

    print('Stopping fake ChromaDB...')
    os.kill(pid, 9)
    print('Fake ChromaDB stopped')

    print('Removing fake ChromaDB...')
    shutil.rmtree('./chroma_fake')
    print('Fake ChromaDB removed')


def chdb_started() -> bool:
    try:
        response = get('http://127.0.0.1:8001/api/v1/heartbeat')
        if response.status_code == 200:
            print('ChromaDB started')
            return True
    except ConnectionError:
        print('Fake ChromaDB not started yet')
        return False

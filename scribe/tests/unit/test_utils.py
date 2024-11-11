import os
import shutil

import pytest

from src.system.utils import JsonEnum


@pytest.fixture(scope='session')
def fake_path():
    fake_dir = './fakedir'
    fake_json_path = os.path.join(fake_dir, 'status.json')
    os.mkdir(fake_dir)
    with open(fake_json_path, 'w') as file:
        file.write('{"status": {"PENDING": "pending", "COMPLETED": "completed", "FAILED": "failed"}}')

    yield fake_json_path

    shutil.rmtree(fake_dir)


def test_enum_is_formed(fake_path):
    StatusEnum = JsonEnum('status', fake_path)

    assert StatusEnum.PENDING.value == "pending"
    assert StatusEnum.COMPLETED.value == "completed"
    assert StatusEnum.FAILED.value == "failed"

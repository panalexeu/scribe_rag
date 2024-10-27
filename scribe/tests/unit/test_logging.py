import os

import pytest
import yaml
from src.system.logging import read_yaml


@pytest.fixture(scope='module')
def get_fake_yaml_file():
    obj = {
        'version': 0,
        'formatters': {
            'dev_file': {
                'format': 'fake'
            }
        }
    }
    fake_path = 'fake.yaml'
    with open(fake_path, 'w') as file:
        file.write(yaml.dump(obj))

    yield obj, fake_path

    os.remove(fake_path)


def test_read_yaml(get_fake_yaml_file):
    obj, fake_path = get_fake_yaml_file

    res = read_yaml(fake_path)

    assert res == obj

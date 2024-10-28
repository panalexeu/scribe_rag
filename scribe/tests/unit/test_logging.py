import os

import pytest
import yaml
from src.system.logging import read_log_config


@pytest.fixture(scope='module')
def get_fake_yaml_file():
    obj = {
        'version': 0,
        'handlers': {
            'file': {
                'filename': 'fake'
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

    res = read_log_config(fake_path, 'fake_log_dir')

    # assert that filename for filehandler in config object is changed for a provided log dir
    assert res != obj
    assert res['handlers']['file']['filename'] != obj['handlers']['file']['filename']
    assert res['handlers']['file']['filename'] == 'fake_log_dir/scribe.log'

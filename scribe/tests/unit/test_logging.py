import os

import pytest
import yaml

from src.system.logging import (
    read_log_config,
    __format_log_file_name
)


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


def test_log_filename_formatting():
    invalid_names = ['log.exe', 'log.log.log', 'test.1', 'test.3']
    valid_names = ['log.log', 'test', '1']

    # if invalid names are provided ValueError is raised
    for invalid_name in invalid_names:
        with pytest.raises(ValueError):
            __format_log_file_name(invalid_name)

    # adds .log extension or if already provided ignores it.
    formatted_valid_names = [__format_log_file_name(valid_name) for valid_name in valid_names]
    assert formatted_valid_names == ['log.log', 'test.log', '1.log']


def test_read_yaml(get_fake_yaml_file):
    obj, fake_path = get_fake_yaml_file

    res = read_log_config(fake_path, 'fake_log_dir', 'fake')

    # assert that filename for filehandler in config object is changed for a provided log dir
    assert res != obj
    assert res['handlers']['file']['filename'] != obj['handlers']['file']['filename']
    assert res['handlers']['file']['filename'] == 'fake_log_dir/fake.log'

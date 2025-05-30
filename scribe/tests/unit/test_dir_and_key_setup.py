import os
import shutil

import pytest

from src.system.dir import (
    get_scribe_dir_path,
    setup_scribe_dir,
    read_scribe_key,
    __clean_scribe_dir,
    __write_scribe_key,
    __clean_log_dir,
    __is_valid_log_file
)


@pytest.fixture(scope='function')
def set_fake_home():
    home = os.environ['HOME']
    os.environ['HOME'] = './fake_dir'
    yield
    os.environ['HOME'] = home


@pytest.fixture(scope='function')
def fake_setup(set_fake_home):
    os.mkdir('./fake_dir')
    scribe_dir = get_scribe_dir_path('.fake')
    yield scribe_dir, os.path.join(scribe_dir, 'fake.key'), os.path.join(scribe_dir, 'fakes'), 'fake-key'
    shutil.rmtree('./fake_dir', ignore_errors=True)


def test_scribe_dir_path_returns(set_fake_home):
    assert get_scribe_dir_path('.fake') == os.path.join(os.environ['HOME'], '.fake')


def test_scribe_dir_sets_up(fake_setup):
    fake_dir, fake_key_file, fake_log_dir, _ = fake_setup
    setup_scribe_dir(*fake_setup)

    assert os.path.exists(fake_dir)
    assert os.path.exists(fake_key_file)
    assert os.path.exists(fake_log_dir)


def test_scribe_dir_is_cleaned_from_unnecessary_files(fake_setup):
    fake_dir, fake_key_file, fake_log_dir, _ = fake_setup
    setup_scribe_dir(*fake_setup)

    # spam files
    with open(os.path.join(fake_dir, 'test1.txt'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_dir, 'test2'), 'w') as file:
        file.write('test')

    # spam nested dirs
    fake_dir_path = os.path.join(fake_dir, 'test_folder')
    os.mkdir(fake_dir_path)
    os.mkdir(os.path.join(fake_dir_path, 'test_folder1'))

    # cleaning
    __clean_scribe_dir(*fake_setup)

    # only scribe.key and logs are left
    scanned_dir = [file.name for file in os.scandir(fake_dir)]

    assert len(scanned_dir) == 2
    assert os.path.exists(fake_key_file)
    assert os.path.exists(fake_log_dir)


def test_is_valid_log_file(fake_setup):
    fake_dir = './fake_dir'

    # spam files
    with open(os.path.join(fake_dir, 'test.txt'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_dir, 'test'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_dir, 'test.exe'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_dir, 'test.ex.3000'), 'w') as file:
        file.write('test')

    # relevant log files
    with open(os.path.join(fake_dir, 'test.log'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_dir, 'test.log.3'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_dir, 'test.log.300'), 'w') as file:
        file.write('test')

    # only three log files are relevant
    valid_files = [__is_valid_log_file(file) for file in os.scandir(fake_dir)]
    assert sum(valid_files) == 3


def test_scribe_logs_dir_is_cleaned_from_unnecessary_files(fake_setup):
    _, _, fake_log_dir, _ = fake_setup
    setup_scribe_dir(*fake_setup)

    # spam files
    with open(os.path.join(fake_log_dir, 'test1.txt'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_log_dir, 'test2.exe'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_log_dir, 'test2'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_log_dir, 'test4.exe.txt'), 'w') as file:
        file.write('test')

    # spam nested dirs
    fake_dir_path = os.path.join(fake_log_dir, 'test_folder')
    os.mkdir(fake_dir_path)
    os.mkdir(os.path.join(fake_dir_path, 'test_folder1'))

    # relevant .log files
    with open(os.path.join(fake_log_dir, 'test1.log'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_log_dir, 'test2.log.1'), 'w') as file:
        file.write('test')

    with open(os.path.join(fake_log_dir, 'test2.log.10'), 'w') as file:
        file.write('test')

    __clean_log_dir(fake_log_dir)

    # only .log files are left
    scanned_dir = [file.name for file in os.scandir(fake_log_dir)]

    assert len(scanned_dir) == 3
    assert os.path.exists(os.path.join(fake_log_dir, 'test1.log'))
    assert os.path.exists(os.path.join(fake_log_dir, 'test2.log.1'))
    assert os.path.exists(os.path.join(fake_log_dir, 'test2.log.10'))


def test_scribe_log_dir_is_recreated(fake_setup):
    fake_dir, _, fake_log_dir, _ = fake_setup
    setup_scribe_dir(*fake_setup)

    # log dir is removed
    os.rmdir(fake_log_dir)

    # after new setup log dir is recreated
    setup_scribe_dir(*fake_setup)

    assert os.path.exists(fake_log_dir)


def test_scribe_dir_recreates_deleted_key_file(fake_setup):
    fake_dir, fake_key_file, fake_log_dir, _ = fake_setup
    setup_scribe_dir(*fake_setup)

    # key deleted
    os.remove(fake_key_file)

    # after new setup key is recreated
    setup_scribe_dir(*fake_setup)

    assert os.path.exists(fake_key_file)


def test_scribe_dir_sets_up_multiple_times(fake_setup):
    fake_dir, fake_key_file, fake_log_dir, _ = fake_setup

    setup_scribe_dir(*fake_setup)

    # spam files in .scribe
    with open(os.path.join(fake_dir, 'test1.txt'), 'w') as file:
        file.write('test')

    fake_dir_path = os.path.join(fake_dir, 'test_folder')
    os.mkdir(fake_dir_path)

    # spam files in .scribe/logs
    with open(os.path.join(fake_log_dir, 'test1.txt'), 'w') as file:
        file.write('test')

    fake_log_dir_path = os.path.join(fake_log_dir, 'test_folder')
    os.mkdir(fake_log_dir_path)

    # relevant .log file in .scribe/logs
    with open(os.path.join(fake_log_dir, 'log.log'), 'w') as file:
        file.write('test')

    # setting folder again
    setup_scribe_dir(*fake_setup)

    # only scribe.key and logs left
    scanned_dir = [file.name for file in os.scandir(fake_dir)]

    assert len(scanned_dir) == 2
    assert os.path.exists(fake_key_file)
    assert os.path.exists(fake_log_dir)

    # in .scribe/logs only log.log is left
    scanned_dir = [file.name for file in os.scandir(fake_log_dir)]

    assert len(scanned_dir) == 1
    assert os.path.exists(os.path.join(fake_log_dir, 'log.log'))

    # setting folder again
    setup_scribe_dir(*fake_setup)

    # nothing has changed
    scanned_dir = [file.name for file in os.scandir(fake_dir)]

    assert len(scanned_dir) == 2
    assert os.path.exists(fake_key_file)
    assert os.path.exists(fake_log_dir)

    scanned_dir = [file.name for file in os.scandir(fake_log_dir)]

    assert len(scanned_dir) == 1
    assert os.path.exists(os.path.join(fake_log_dir, 'log.log'))


def test_keys_are_the_same_after_multiple_set_ups(fake_setup):
    fake_dir, fake_key_file, fake_log_dir, _ = fake_setup

    setup_scribe_dir(*fake_setup)
    key = read_scribe_key(fake_key_file)

    # spam files and dirs
    with open(os.path.join(fake_dir, 'test1.txt'), 'w') as file:
        file.write('test')

    fake_dir_path = os.path.join(fake_dir, 'test_folder')
    os.mkdir(fake_dir_path)

    # setting folder again
    setup_scribe_dir(*fake_setup)
    key_new = read_scribe_key(fake_key_file)

    assert key == key_new


def test_read_and_write_scribe_key(fake_setup):
    fake_dir, fake_key_file, fake_log_dir, fake_key = fake_setup

    os.mkdir(fake_dir)

    # key file has been written
    __write_scribe_key(fake_key_file, fake_key)
    assert os.path.exists(fake_key_file)

    # key file is successfully retrieved
    read_key = read_scribe_key(fake_key_file)
    assert read_key == fake_key

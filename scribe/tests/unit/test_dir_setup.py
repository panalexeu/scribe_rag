import os
import shutil

import pytest

from src.system.dir import (
    get_scribe_folder_path,
    setup_scribe_folder,
    clean_scribe_folder,
    write_scribe_key,
    read_scribe_key,
    KEY_FILE,
    validate_key
)


@pytest.fixture(scope='module')
def set_fake_home_path():
    os.environ['HOME'] = './fake_folder'
    os.mkdir('./fake_folder')
    yield
    shutil.rmtree('./fake_folder', ignore_errors=True)


def test_scribe_folder_path_returns(set_fake_home_path):
    assert get_scribe_folder_path() == os.path.join(os.environ['HOME'], '.scribe')


def test_scribe_folder_sets_up(set_fake_home_path):
    setup_scribe_folder()
    fake_home_path = os.path.join(os.environ['HOME'], '.scribe')

    assert os.path.exists(os.path.join(fake_home_path, KEY_FILE))
    assert os.path.exists(fake_home_path)


def test_scribe_folder_is_cleaned_from_unnecessary_files(set_fake_home_path):
    setup_scribe_folder()

    # spam files
    with open(os.path.join(get_scribe_folder_path(), 'test1.txt'), 'w') as file:
        file.write('test')

    with open(os.path.join(get_scribe_folder_path(), 'test2'), 'w') as file:
        file.write('test')

    # spam nested dirs
    fake_dir_path = os.path.join(get_scribe_folder_path(), 'test_folder')
    os.mkdir(fake_dir_path)
    os.mkdir(os.path.join(fake_dir_path, 'test_folder1'))

    # cleaning
    clean_scribe_folder()

    # only scribe.key is left
    scanned_dir = [file.name for file in os.scandir(get_scribe_folder_path())]

    assert len(scanned_dir) == 1
    assert scanned_dir[0] == KEY_FILE


def test_scribe_folder_sets_up_multiple_times():
    setup_scribe_folder()

    # spam files and dirs
    with open(os.path.join(get_scribe_folder_path(), 'test1.txt'), 'w') as file:
        file.write('test')

    fake_dir_path = os.path.join(get_scribe_folder_path(), 'test_folder')
    os.mkdir(fake_dir_path)

    # setting folder again
    setup_scribe_folder()

    # only scribe.key is left
    scanned_dir = [file.name for file in os.scandir(get_scribe_folder_path())]

    assert len(scanned_dir) == 1
    assert scanned_dir[0] == KEY_FILE

    # setting folder again
    setup_scribe_folder()

    # nothing has changed
    scanned_dir = [file.name for file in os.scandir(get_scribe_folder_path())]

    assert len(scanned_dir) == 1
    assert scanned_dir[0] == KEY_FILE


def test_read_and_write_of_scribe_key(set_fake_home_path):
    key = write_scribe_key()

    assert os.path.exists(os.path.join(get_scribe_folder_path(), KEY_FILE))

    read_key = read_scribe_key()

    assert read_key == key


def test_validate_key():
    with pytest.raises(ValueError):
        validate_key('привіт')

    with pytest.raises(ValueError):
        validate_key('ASDasdADmklasd123{}1@')

    with pytest.raises(ValueError):
        validate_key("""
            adsds 
             sad
            123 * ? 
        """)

    assert validate_key('LvHrHVBQN1iyTpJHHqCGx1t9SWdG-dyWT3qjnlj99iQ=') is None

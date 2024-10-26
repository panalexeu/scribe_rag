import os
import shutil

import pytest

from src.system.dir import (
    get_scribe_dir_path,
    setup_scribe_dir,
    clean_scribe_dir,
    write_scribe_key,
    read_scribe_key,
    validate_key,
    get_scribe_key_file
)


@pytest.fixture(scope='module')
def fake_setup():
    os.environ['HOME'] = './fake_dir'
    os.mkdir('./fake_dir')
    yield get_scribe_dir_path(), get_scribe_key_file()
    shutil.rmtree('./fake_dir', ignore_errors=True)


def test_scribe_folder_path_returns():
    os.environ['HOME'] = './fake_dir'
    assert get_scribe_dir_path() == os.path.join(os.environ['HOME'], '.scribe')


def test_scribe_key_path_returns():
    os.environ['HOME'] = './fake_dir'

    assert get_scribe_key_file() == os.path.join(os.environ['HOME'], '.scribe', 'scribe.key')


def test_scribe_folder_sets_up(fake_setup):
    fake_dir, fake_key_file = fake_setup
    setup_scribe_dir(*fake_setup)
    fake_home_path = os.path.join(os.environ['HOME'], '.scribe')

    assert os.path.exists(fake_key_file)
    assert os.path.exists(fake_home_path)


def test_scribe_folder_is_cleaned_from_unnecessary_files(fake_setup):
    fake_dir, fake_key_file = fake_setup
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
    clean_scribe_dir(*fake_setup)

    # only scribe.key is left
    scanned_dir = [file.name for file in os.scandir(fake_dir)]

    assert len(scanned_dir) == 1
    assert scanned_dir[0] == os.path.basename(fake_key_file)


def test_scribe_folder_recreates_deleted_key_file(fake_setup):
    fake_dir, fake_key_file = fake_setup
    setup_scribe_dir(*fake_setup)

    # key deleted
    os.remove(fake_key_file)

    setup_scribe_dir(*fake_setup)

    assert os.path.exists(fake_key_file)


def test_scribe_folder_rewrites_changed_invalid_key(fake_setup):
    fake_dir, fake_key_file = fake_setup

    # initial key
    setup_scribe_dir(*fake_setup)
    read_scribe_key(fake_key_file)

    # key rewritten
    with open(fake_key_file, 'w') as file:
        file.write('bla, bla')

    with pytest.raises(ValueError):
        read_scribe_key(fake_key_file)

    # key recreated
    setup_scribe_dir(*fake_setup)
    read_scribe_key(fake_key_file)


def test_scribe_folder_sets_up_multiple_times_and_saves_key(fake_setup):
    fake_dir, fake_key_file = fake_setup

    setup_scribe_dir(*fake_setup)

    # spam files and dirs
    with open(os.path.join(fake_dir, 'test1.txt'), 'w') as file:
        file.write('test')

    fake_dir_path = os.path.join(fake_dir, 'test_folder')
    os.mkdir(fake_dir_path)

    # setting folder again
    setup_scribe_dir(*fake_setup)

    # only scribe.key is left
    scanned_dir = [file.name for file in os.scandir(fake_dir)]

    assert len(scanned_dir) == 1
    assert scanned_dir[0] == os.path.basename(fake_key_file)

    # setting folder again
    setup_scribe_dir(*fake_setup)

    # nothing has changed
    scanned_dir = [file.name for file in os.scandir(fake_dir)]

    assert len(scanned_dir) == 1
    assert scanned_dir[0] == os.path.basename(fake_key_file)


def test_keys_are_the_same_after_multiple_set_ups(fake_setup):
    fake_dir, fake_key_file = fake_setup

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
    fake_dir, fake_key_file = fake_setup

    key = write_scribe_key(fake_key_file)

    assert os.path.exists(os.path.join(fake_key_file))

    read_key = read_scribe_key(fake_key_file)

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

    validate_key('LvHrHVBQN1iyTpJHHqCGx1t9SWdG-dyWT3qjnlj99iQ=')

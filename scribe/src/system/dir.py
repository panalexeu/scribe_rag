import os
from os import DirEntry
import shutil

from cryptography.fernet import Fernet


def setup_scribe_dir(
        scribe_dir: str,
        scribe_key_file: str,
        log_dir: str,
        key: str
) -> None:
    """
    Sets up .scribe folder in $HOME directory. If the folder exists, cleans it.

    :raises OSError:
    """
    if os.path.exists(scribe_dir):
        __clean_scribe_dir(scribe_dir, scribe_key_file, log_dir, key)
        return

    # setting up directories and key file
    os.mkdir(scribe_dir)
    os.mkdir(log_dir)
    __write_scribe_key(scribe_key_file, key)


def get_scribe_dir_path(dir_name: str) -> str:
    """
    :returns: str - $HOME/'dir_name' file path.
    """
    home = os.environ['HOME']
    scribe_path = os.path.join(home, dir_name)

    return scribe_path


def read_scribe_key(
        scribe_key_file: str
) -> str:
    """
    Reads scribe.key file.

    :raises FileNotFoundError: If key file is not found.
    """
    with open(scribe_key_file, 'r') as file:
        key = file.read()

    return key


def __clean_scribe_dir(
        scribe_dir: str,
        scribe_key_file: str,
        log_dir: str,
        key: str
) -> None:
    """
    Cleans $HOME/.scribe dir, leaving only 'scribe.key' file and logs dir. Rewrites deleted or
    changed 'scribe.key' file. Cleans logs directory content.

    :raises OSError:
    """

    # cleaning
    with os.scandir(scribe_dir) as scan:
        for file in scan:
            if file.is_dir() and file.name != os.path.basename(log_dir):
                shutil.rmtree(os.path.join(scribe_dir, file.name))
            elif file.is_file() and file.name != os.path.basename(scribe_key_file):
                os.remove(file)

    # handling key file
    if not os.path.exists(scribe_key_file):
        __write_scribe_key(scribe_key_file, key)

    # handling log dir
    if os.path.exists(log_dir):
        __clean_log_dir(log_dir)
    else:
        os.mkdir(log_dir)


def __clean_log_dir(log_dir: str) -> None:
    """
    Cleans $HOME/.scribe/logs directory from not *.log files or directories.

    :raises OSError:
    """
    with os.scandir(log_dir) as scan:
        for file in scan:
            if file.is_dir():
                shutil.rmtree(os.path.join(log_dir, file.name))
            elif not __is_valid_log_file(file):
                os.remove(file)


def __is_valid_log_file(file: DirEntry) -> bool:
    """
    :returns: bool - If a file has extension of *.log or *.log.1, ... *.log.n
    """
    file = os.path.basename(file)
    split_file: list[str] = file.split('.')

    match len(split_file):
        case 2:
            return split_file[-1] == 'log'
        case 3:
            return split_file[-2] == 'log' and split_file[-1].isdigit()
        case _:
            return False


def __write_scribe_key(
        scribe_key_file: str,
        key: str
) -> None:
    with open(scribe_key_file, 'w') as file:
        file.write(key)

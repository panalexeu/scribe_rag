import os
from os import DirEntry
import shutil

from cryptography.fernet import Fernet


def setup_scribe_dir(
        scribe_dir: str,
        scribe_key_file: str,
        log_dir: str
) -> None:
    """
    Sets up .scribe folder in $HOME directory. If the folder exists, cleans it.

    :raises OSError:
    """
    if os.path.exists(scribe_dir):
        __clean_scribe_dir(scribe_dir, scribe_key_file, log_dir)
        return

    # setting up directories and key file
    os.mkdir(scribe_dir)
    os.mkdir(log_dir)
    __write_scribe_key(scribe_key_file)


def get_scribe_dir_path(dir_name: str) -> str:
    """
    :returns: str - $HOME/'dir_name' file path.
    """
    home = os.environ['HOME']
    scribe_path = os.path.join(home, dir_name)

    return scribe_path


def get_scribe_log_dir_path(
        scribe_dir: str,
        log_dir_name: str
) -> str:
    """
    :returns: str - 'scribe_dir'/'log_dir_name' file path.
    """
    log_path = os.path.join(scribe_dir, log_dir_name)

    return log_path


def get_scribe_key_file(
        scribe_dir: str,
        key_name: str
) -> str:
    """
    :returns: str - 'scribe_dir'/'key_name' file path.
    """
    key_path = os.path.join(scribe_dir, key_name)

    return key_path


def read_scribe_key(
        scribe_key_file: str
) -> str:
    """
    Reads scribe.key file.

    :raises FileNotFoundError: If key file is not found.
    :raises ValueError: If key is not valid.
    """

    with open(scribe_key_file, 'r') as file:
        key = file.read()
        __validate_key(key)

    return key


def __clean_scribe_dir(
        scribe_dir: str,
        scribe_key_file: str,
        log_dir: str
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
    if os.path.exists(scribe_key_file):
        try:
            read_scribe_key(scribe_key_file)
        except ValueError:
            __write_scribe_key(scribe_key_file)
    else:
        __write_scribe_key(scribe_key_file)

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
        scribe_key_file: str
) -> str:
    """
    Writes base64-encoded (base64.urlsafe_b64encode) 32-byte generated key (os.urandom).

    :returns: str - A generated base64-encoded 32-byte key.

    :raises OSError:
    """
    key: bytes = Fernet.generate_key()
    key_to_str: str = key.decode()

    with open(scribe_key_file, 'w') as file:
        file.write(key_to_str)

    return key_to_str


def __validate_key(key: str) -> None:
    """
    Validates Fernet generated key.

    :raises ValueError: If provided key is not valid base64 encoded 32 byte key.
    """

    Fernet(key)

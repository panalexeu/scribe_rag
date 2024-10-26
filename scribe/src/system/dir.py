import os
import shutil

from cryptography.fernet import Fernet


def setup_scribe_dir(
        scribe_dir: str,
        scribe_key_file: str
) -> None:
    """
    Sets up .scribe folder in $HOME directory. If the folder exists, cleans it.
    """
    if os.path.exists(scribe_dir):
        __clean_scribe_dir(scribe_dir, scribe_key_file)
        return

    os.mkdir(scribe_dir)
    __write_scribe_key(scribe_key_file)


def get_scribe_dir_path() -> str:
    """
    :return: str - $HOME/.scribe file path.
    """
    home = os.environ['HOME']
    scribe_path = os.path.join(home, '.scribe')

    return scribe_path


def get_scribe_key_file() -> str:
    """
    :return: str - $HOME/.scribe/scribe.key file path.
    """
    key_path = os.path.join(os.environ.get('HOME'), '.scribe', 'scribe.key')

    return key_path


def __clean_scribe_dir(
        scribe_dir: str,
        scribe_key_file: str
) -> None:
    """
    Cleans $HOME/.scribe dir, leaving only 'scribe.key' file. Rewrites deleted or changed 'scribe.key' file.
    """

    with os.scandir(scribe_dir) as scan:
        for file in scan:
            if file.is_dir():
                shutil.rmtree(os.path.join(scribe_dir, file.name))
            else:
                if file.name != os.path.basename(scribe_key_file):
                    os.remove(file)

    if os.path.exists(scribe_key_file):
        try:
            __read_scribe_key(scribe_key_file)
        except ValueError:
            __write_scribe_key(scribe_key_file)
    else:
        __write_scribe_key(scribe_key_file)


def __write_scribe_key(
        scribe_key_file: str
) -> str:
    """
    Writes base64-encoded (base64.urlsafe_b64encode) 32-byte generated key (os.urandom).

    :returns: str - A generated base64-encoded 32-byte key.
    """
    key: bytes = Fernet.generate_key()
    key_to_str: str = key.decode()

    with open(scribe_key_file, 'w') as file:
        file.write(key_to_str)

    return key_to_str


def __read_scribe_key(
        scribe_key_file: str
) -> str:
    """Reads scribe.key file."""

    with open(scribe_key_file, 'r') as file:
        key = file.read()
        __validate_key(key)

    return key


def __validate_key(key: str) -> None:
    """
    Validates Fernet generated key.
    """

    Fernet(key)

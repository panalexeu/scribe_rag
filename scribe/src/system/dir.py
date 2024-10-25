import os
import shutil

from cryptography.fernet import Fernet

DIR = '.scribe'
KEY_FILE = 'scribe.key'


def setup_scribe_folder() -> None:
    """
    Sets up .scribe folder in $HOME directory.
    If the folder exists, cleans it leaving only 'scribe.key' file.
    """
    if os.path.exists(get_scribe_folder_path()):
        clean_scribe_folder()
        return

    os.mkdir(get_scribe_folder_path())
    write_scribe_key()


def clean_scribe_folder() -> None:
    """
    Cleans $HOME/.scribe dir, leaving only 'scribe.key' file.
    """

    with os.scandir(get_scribe_folder_path()) as scan:
        for file in scan:
            if file.is_dir():
                shutil.rmtree(os.path.join(get_scribe_folder_path(), file.name))
            else:
                if file.name != KEY_FILE:
                    os.remove(file)


def get_scribe_folder_path() -> str:
    """
    Returns $HOME/.scribe file path

    :return: str
    """
    home = os.environ['HOME']
    scribe_path = os.path.join(home, DIR)

    return scribe_path


def write_scribe_key() -> str:
    """
    Writes base64-encoded (base64.urlsafe_b64encode) 32-byte generated key (os.urandom).

    :returns: str - A generated base64-encoded 32-byte key.
    """
    key: bytes = Fernet.generate_key()
    key_to_str: str = key.decode()
    key_file = os.path.join(get_scribe_folder_path(), KEY_FILE)

    with open(key_file, 'w') as file:
        file.write(key_to_str)

    return key_to_str


def read_scribe_key() -> str:
    key_file = os.path.join(get_scribe_folder_path(), KEY_FILE)

    with open(key_file, 'r') as file:
        key = file.read()
        validate_key(key)

    return key


def validate_key(key: str) -> None:
    Fernet(key)

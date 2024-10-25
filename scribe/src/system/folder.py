import os
import shutil

from .encr import KEY_FILE


def setup_scribe_folder():
    """
    Sets up .scribe folder in $HOME directory.
    If the folder exists, cleans it leaving only 'scribe.key' file.
    """
    if os.path.exists(get_scribe_folder_path()):
        clean_scribe_folder()
        return

    os.mkdir(get_scribe_folder_path())


def clean_scribe_folder():
    """
    Cleans $HOME/.scribe dir, leaving only 'scribe.key' file.
    """

    for file in os.scandir(get_scribe_folder_path()):
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
    scribe_path = os.path.join(home, '.scribe')

    return scribe_path

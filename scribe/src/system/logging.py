import os.path

import yaml


def read_log_config(
        config_path: str,
        log_dir: str,
        log_file_name: str
) -> dict:
    """
    Parses provided *.yaml logging config. Sets filename value for
    the file handler with the 'log_dir'/'log_file_name'.
    """
    # formatting log file name
    formatted_log_file_name = __format_log_file_name(log_file_name)

    with open(config_path, 'r') as file:
        obj = yaml.safe_load(file.read())
        # replacing 'placeholder' with an actual value
        obj['handlers']['file']['filename'] = os.path.join(log_dir, formatted_log_file_name)

        return obj


def __format_log_file_name(file_name: str) -> str:
    """
    Adds .log extension if not provided to the 'file_name'.

    :returns: str - A formatted 'file_name' with a .log extension.
    :raises ValueError: If the 'file_name' with an extension other than .log is provided.
    """
    extension = '.log'

    split_log_file_name = file_name.split('.')
    match len(split_log_file_name):
        case 1:
            return str(split_log_file_name[0]) + extension
        case 2:
            if split_log_file_name[-1] == 'log':
                return file_name

    raise ValueError(f'Invalid log file name "{file_name}" is provided')

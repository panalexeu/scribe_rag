import os.path

import yaml


def read_log_config(
        config_path: str,
        log_dir: str
) -> dict:
    """
    Parses provided *.yaml logging config. Sets filename value for
    the file handler with the 'log_dir'/scribe.log.
    """

    with open(config_path, 'r') as file:
        obj = yaml.safe_load(file.read())
        # replacing 'placeholder' with an actual value
        obj['handlers']['file']['filename'] = os.path.join(log_dir, 'scribe.log')

        return obj

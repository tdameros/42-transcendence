import logging

from colorlog import ColoredFormatter

import src.shared_code.settings as settings


def create_log_formatter():
    return ColoredFormatter(
        "%(log_color)s%(levelname)-8s %(asctime)s:%(reset)s %(message)s",
        datefmt="%Hh:%Mm:%Ss",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )


def setup_logging():
    formatter = create_log_formatter()

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)

    logger.setLevel(settings.LOG_LEVEL)

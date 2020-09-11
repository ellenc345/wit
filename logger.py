import logging
import os
from pathlib import Path

from consts import ERROR_LOG, REPOSITORY_FOLDER


def define_logging(name):
    FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
    formatter = logging.Formatter(FORMAT)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Add logging to file
    file_handler = logging.FileHandler(Path(REPOSITORY_FOLDER, ERROR_LOG))
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Add info logging to cmd
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

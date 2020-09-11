import logging
import os
from pathlib import Path

from consts import (IMAGES_FOLDER, REPOSITORY_FOLDER,
                    STAGING_FOLDER, ACTIVE_BRANCH_FILE)

from helpers import validate_before_init


def init():
    """This function will create essentioal olders for wit."""
    repository_folder_path = os.path.join(os.getcwd(), REPOSITORY_FOLDER)
    images_folder_path = os.path.join(
        os.getcwd(), REPOSITORY_FOLDER, IMAGES_FOLDER)
    staging_folder_path = os.path.join(
        os.getcwd(), REPOSITORY_FOLDER, STAGING_FOLDER)
    try:
        if validate_before_init(repository_folder_path):
            os.mkdir(repository_folder_path)
            os.mkdir(images_folder_path)
            os.mkdir(staging_folder_path)
            create_active_branch()

    except (OSError, TypeError) as err:
        logging.error(f'{err}\nAborted')


def create_active_branch():
    Path(REPOSITORY_FOLDER, ACTIVE_BRANCH_FILE).open('w').write('master')

import os
import shutil
from pathlib import Path

from consts import REPOSITORY_FOLDER, STAGING_FOLDER

from helpers import get_wit_repo_path

from wit_errors import WitFileNotFound


def add(relative_path_to_add, destination=None, keep_destination=False):
    """This method will stage the selected file or directory."""
    if not destination:
        destination = Path(REPOSITORY_FOLDER, STAGING_FOLDER)
    path_to_add = Path(os.getcwd(), relative_path_to_add)

    # Check if file exist
    if not Path(path_to_add).exists():
        raise WitFileNotFound(path_to_add)

    if not Path(destination).exists():
        raise WitFileNotFound(destination)

    # Identify the nearest .wit folder
    get_wit_repo_path(path_to_add)

    if path_to_add.is_file():
        dest = Path(destination, relative_path_to_add).parent
        if not dest.exists():
            os.makedirs(dest)
        shutil.copy2(path_to_add, dest)
    elif keep_destination:
        shutil.copytree(path_to_add, destination, dirs_exist_ok=True)
    else:
        files_container = Path(destination, relative_path_to_add)
        shutil.copytree(path_to_add, files_container, dirs_exist_ok=True)

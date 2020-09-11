from wit_errors import UncommitedChangesError
import shutil
from pathlib import Path

from consts import (IMAGES_FOLDER, STAGING_FOLDER)

from handlers.status import get_staged_files, get_unstaged_files

from helpers import (get_wit_repo_path, get_commit_by_branch,
                     activate_branch, update_ref)


def checkout(commit_id_or_branch):
    """
    This function will restore the image in the relevant commit_id folder
    """

    # Find the repository
    repository_path = get_wit_repo_path()

    commit_id = resolve_commit_id(commit_id_or_branch)

    # Fail if there is staged files or track files has been changed
    currend_head = get_commit_by_branch('HEAD')
    if (len(get_staged_files(repository_path, currend_head))
            or len(list(get_unstaged_files(repository_path)))):

        raise UncommitedChangesError()

    # Restore origin files to image state
    image_folder = Path(
        repository_path, IMAGES_FOLDER, commit_id)
    shutil.copytree(image_folder, repository_path.parent, dirs_exist_ok=True)

    # Restore the staging area to image state
    # Ignore deleted files at this point,
    # so all files should be in staging folder.
    shutil.copytree(image_folder, Path(repository_path,
                                       STAGING_FOLDER), dirs_exist_ok=True)

    # Update the HEAD
    update_ref('HEAD', commit_id)
    activate_branch(resolve_branch_name(commit_id_or_branch))


def resolve_commit_id(param):
    commit_id = get_commit_by_branch(param)
    if commit_id is not None:
        return commit_id
    else:
        return param


def resolve_branch_name(commit_id_or_branch):
    # if comit id suppordet, the branch will be None
    if get_commit_by_branch(commit_id_or_branch):
        return commit_id_or_branch
    return None

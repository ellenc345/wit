
import filecmp
import os
from pathlib import Path, PurePath

from consts import (IMAGES_FOLDER, REFERENCE_FILE,
                    REPOSITORY_FOLDER, STAGING_FOLDER)

from helpers import get_commit_by_branch, get_wit_repo_path
from logger import define_logging
from wit_errors import WitCommitNotFound


def status():
    """This function will retrive the repository status.
    Usage:
    python path/to/wit.py status
    """
    logger = define_logging(__name__)
    # Find the repository
    repository_path = get_wit_repo_path()

    head = get_commit_by_branch('HEAD')
    staged_files = get_staged_files(repository_path, head)
    not_staged_changes = list(
        get_unstaged_files(repository_path))
    untracked_files = get_untracked_files(repository_path, staged_files)

    logger.info(f'HEAD: {head}')
    logger.info(
        f'Changes to be committed ({len(staged_files)}) :\n{format_list(staged_files)}')
    logger.info(
        f'Changes not staged for commit ({len(not_staged_changes)}) :\n{format_list(not_staged_changes)}')
    logger.info(
        f'Untracked files ({len(untracked_files)}) :\n{format_list(untracked_files)}')
    return


def get_untracked_files(repository_path, staged_files):
    all_files = list(get_relative_paths(repository_path.parent))
    untraked = list(filter(lambda file_: filter_untracked(
        file_, repository_path), all_files))
    return list(map(lambda rel_path: PurePath(repository_path.parent, rel_path), untraked))


def filter_untracked(file_, repository_path):
    # not a wit file and not staged
    if (file_.parts[0] == REPOSITORY_FOLDER
            or Path(repository_path, STAGING_FOLDER, file_).exists()):
        return False
    return True


def get_staged_files(repository_path, head):
    """Returns all the staged for the next commit files.
    that means that they was changed and added."""
    # get all files in staging area
    original_path = Path(repository_path).parent
    all_files_in_staging_area = get_staged_relative_pathes(repository_path)

    # get an image folder to refer
    last_commited_image_folder = None
    if not Path(repository_path, REFERENCE_FILE).exists():
        staged_files = all_files_in_staging_area

    else:
        try:
            last_commited_image_folder = Path(repository_path,
                                              IMAGES_FOLDER, head)
        except (OSError) as err:
            raise WitCommitNotFound(err)

        # filter the unchanged files
        staged_files = list(filter_unchanged(all_files_in_staging_area,
                                             Path(repository_path,
                                                  STAGING_FOLDER),
                                             last_commited_image_folder))

    return list(map(lambda rel_path: PurePath(original_path,
                                              rel_path), staged_files))


def filter_unchanged(files_to_filter, origin_folder, reference_folder=None):
    # return only files that were modified from the taken image
    if not reference_folder:
        return files_to_filter

    for file_ in files_to_filter:
        ref_file = Path(reference_folder, file_)
        origin_file = Path(origin_folder, file_)

        if not (ref_file.exists()
                and filecmp.cmp(ref_file, origin_file, shallow=False)):
            yield file_


def get_unstaged_files(repository_path):
    """Return all the not staged files.
    that means files that was changed and were not added"""

    staging_prefix = PurePath(repository_path, STAGING_FOLDER)
    original_path = PurePath(repository_path).parent
    unstaged_files = get_staged_relative_pathes(repository_path)

    for file_ in unstaged_files:
        origin_file = PurePath(original_path, file_)
        staged_file = PurePath(staging_prefix, file_)
        if not filecmp.cmp(origin_file, staged_file, shallow=False):
            yield origin_file


def get_staged_relative_pathes(repository_path, relative_to=''):
    staging_folder = PurePath(repository_path, STAGING_FOLDER)
    relative_paths = list(get_relative_paths(staging_folder))
    return list(map(lambda rel_path: PurePath(relative_to, rel_path),
                    relative_paths))


def get_relative_paths(root):
    for dirpath, _, files in os.walk(root):
        for file_name in files:
            relative_path = make_relative_to_repo(
                Path(dirpath, file_name), root)
            yield relative_path


def make_relative_to_repo(absolute_path, substract):
    parts = absolute_path.parts[len(substract.parts):]
    return PurePath(*parts)


def format_list(things):
    str_ = ''
    for item in things:
        str_ += f'{str(item)}\n'
    return str_

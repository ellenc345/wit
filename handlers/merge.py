import filecmp
import shutil
from pathlib import Path

from consts import IMAGES_FOLDER, STAGING_FOLDER
from helpers import get_active_branch, get_commit_by_branch, get_wit_repo_path
from wit_errors import WitCommitNotFound

from handlers.commit import commit
from handlers.status import get_relative_paths, make_relative_to_repo


def merge(destination_branch):
    """This function will create new commit that contains
    teh changes from the curent active branch and the destination branch"""
    repository_path = get_wit_repo_path()

    lca = find_lowest_common_anccestor(repository_path,
                                       'HEAD', destination_branch)
    print(lca)

    # get changed files from lca (lowest common anccestor commit)
    changed = list(
        get_all_changed_files(repository_path,
                              lca,
                              get_commit_by_branch(destination_branch)))

    # replace the changed files into the staging area and commit them
    for file_ in changed:
        original_file = Path(repository_path, IMAGES_FOLDER,
                             get_commit_by_branch(destination_branch), file_)
        destination = Path(repository_path, STAGING_FOLDER, file_)
        shutil.copy2(original_file, destination)

    commit(f"mrege: branch {get_active_branch()}",
           additional_parents=list(destination_branch))


# def make_relative_to_repo(absolute_path, substract):
#     parts = absolute_path.parts[len(substract.parts):]
#     return PurePath(*parts)


def get_all_changed_files(repository_path, commit_id_1, commit_id_2):
    base_folder = Path(repository_path, IMAGES_FOLDER, commit_id_1)
    latest_folfer = Path(repository_path, IMAGES_FOLDER, commit_id_2)
    files_ = list(get_relative_paths(latest_folfer))

    for file_ in files_:
        old_file = Path(base_folder, file_)
        new_file = Path(latest_folfer, file_)
        if not old_file.exists():
            yield file_
        elif not filecmp.cmp(new_file, old_file):
            yield file_


def find_lowest_common_anccestor(repository_path, branch_1, branch_2):
    # Go up in the hirrchy and save the commit id in a set
    # if it already exist in the set this is the LCA

    if get_commit_by_branch(branch_1) == get_commit_by_branch(branch_2):
        return get_commit_by_branch(branch_1)

    parents_cash = set()
    parents_to_traverse = [get_commit_by_branch(branch_1)]

    while len(parents_to_traverse):
        current_node = parents_to_traverse.pop()
        parents_cash.add(current_node)
        for parent in get_parents(repository_path, current_node):
            if parent != 'None':
                parents_to_traverse.append(parent)

    parents_to_traverse = [get_commit_by_branch(branch_2)]

    while len(parents_to_traverse):
        current_node = parents_to_traverse.pop()
        if current_node != 'None':
            if current_node in parents_cash:
                return current_node
            else:
                for parent in get_parents(repository_path, current_node):
                    parents_to_traverse.append(parent)
                    if parent == 'None':
                        return None


def get_parents(repository_path, commit_id):
    info_file = Path(repository_path, IMAGES_FOLDER,
                     commit_id).with_suffix('.txt')
    if not info_file.exists():
        raise WitCommitNotFound()
    return read_parents(info_file)


def read_parents(file):
    info = file.open().read().split()
    return (list(filter(lambda row: "parent" in row, info))[0]
            .split("=")[1].split(','))

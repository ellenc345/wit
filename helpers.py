import os
import random
from pathlib import Path, PurePath

from consts import REPOSITORY_FOLDER, REFERENCE_FILE, ACTIVE_BRANCH_FILE

from wit_errors import WitFileNotFound, WitRepositoryNotFound


def generate_id():
    return ''.join(random.choice('0123456789abcdef') for _ in range(40))


def get_wit_repo_path(path=None):
    if(not path):
        path = os.getcwd()

    current_search_path = Path(path)
    if(current_search_path.is_file()):
        current_search_path = current_search_path.parent

    # Search .wit filder bottom up
    most_upper_folder = PurePath().parent
    while (current_search_path != most_upper_folder):
        repository_folder = Path(
            PurePath(current_search_path, REPOSITORY_FOLDER))
        if repository_folder.exists():
            return repository_folder

        current_search_path = Path(current_search_path).parent
    raise WitRepositoryNotFound()


def validate_before_init(path):
    if Path(path).is_dir():
        raise OSError(f'wit already initialized {path}')
    return True


def get_commit_by_branch(branch):
    reference = Path(REPOSITORY_FOLDER, REFERENCE_FILE)
    if(reference.exists()):
        ref = reference.read_text().split()
        found_ref = list(filter(lambda row: branch in row, ref))
        if len(found_ref):
            latest_commit_id = found_ref[0].split('=')[1]
            return latest_commit_id
    return None


def get_branchs_by_commit(commit_id):
    reference = Path(REPOSITORY_FOLDER, REFERENCE_FILE)
    if(reference.exists()):
        ref = reference.read_text().split()
        branches = list(filter(lambda row: commit_id in row, ref))[0]
        for branch in branches:
            yield branch.split('=')[0]
    else:
        yield None


def update_ref(branch_to_update, new_commit_id):
    reference = Path(REPOSITORY_FOLDER, REFERENCE_FILE)
    if reference.exists():
        refs = reference.read_text().split()
        new_ref_file = Path(REPOSITORY_FOLDER, f'new_{REFERENCE_FILE}')
        for ref in refs:
            if ref.split("=")[0] == branch_to_update:
                new_ref_file.open('a', newline='\n').write(
                    f'{branch_to_update}={new_commit_id}\n')
            else:
                new_ref_file.open('a', newline='\n').write(f'{ref}\n')
        reference.unlink()
        new_ref_file.replace(reference)
    else:
        raise WitFileNotFound()


def add_ref(branch, commit_id):
    reference = Path(REPOSITORY_FOLDER, REFERENCE_FILE)
    reference.open('a').write(f'{branch}={commit_id}')


def activate_branch(branch):
    Path(REPOSITORY_FOLDER, ACTIVE_BRANCH_FILE).open('w').write(branch)


def get_active_branch():
    return Path(REPOSITORY_FOLDER, ACTIVE_BRANCH_FILE).read_text()


def get_all_branches():
    reference = Path(REPOSITORY_FOLDER, REFERENCE_FILE)
    all_refs = reference.read_text().split()
    for ref in all_refs:
        yield ref.split('=')[0]

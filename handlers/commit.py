from datetime import datetime
from pathlib import Path, PurePath

from consts import (IMAGES_FOLDER, REFERENCE_FILE, REPOSITORY_FOLDER,
                    STAGING_FOLDER)

from handlers.add import add

from helpers import (generate_id, get_wit_repo_path,
                     get_commit_by_branch, get_active_branch, update_ref)
from handlers.status import get_staged_files


def commit(message, additional_parents=None):
    """
    This function will copy an "image" to the IMAGES_FOLDER
    and will add an reference file if needed
    """

    # Find the repository
    repository_path = get_wit_repo_path()

    # proceed only if there is staged files
    if len(get_staged_files
            (repository_path, head=get_commit_by_branch('HEAD'))) == 0:
        return

    # create image folder
    commit_id = generate_id()
    current_image_folder = Path(repository_path, IMAGES_FOLDER, commit_id)
    Path.mkdir(current_image_folder)

    # create metedata
    create_metadate_file(current_image_folder.parent,
                         commit_id, message, additional_parents)

    # add all files
    add(relative_path_to_add=PurePath(REPOSITORY_FOLDER, STAGING_FOLDER),
        destination=current_image_folder, keep_destination=True)

    # update reference
    reference_file = Path(REPOSITORY_FOLDER, REFERENCE_FILE)
    if not reference_file.exists():
        init_reference(reference_file, commit_id)
    else:
        update_reference(commit_id)


def create_metadate_file(path, commit_id, message, additional_parents):
    metadata = create_metadata(message, additional_parents)
    metadata_file = Path(path, f'{commit_id}.txt')
    metadata_file.open('w').write(metadata)


def create_metadata(message, additional_parents):
    parents = get_commit_by_branch('HEAD')
    if additional_parents:
        parents = ",".join([str(parents)].extend([additional_parents]))
    return f'parent={parents}\ndate={datetime.now()}\nmessage={message}\n'


def update_reference(commit_id):
    update_branch_if_needed(commit_id)

    update_ref('HEAD', commit_id)


def init_reference(reference_file, commit_id):
    ref = f'HEAD={commit_id}\nmaster={commit_id}\n'
    reference_file.open('w').write(ref)


def update_branch_if_needed(commit_id):
    # If the active branch is same as the head,
    # Update branch
    active_branch = get_active_branch()
    head = get_commit_by_branch('HEAD')
    if get_commit_by_branch(active_branch) == head:
        update_ref(active_branch, commit_id)

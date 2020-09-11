from helpers import get_wit_repo_path, get_commit_by_branch, add_ref


def branch(branch_name):

    # Find the repository
    get_wit_repo_path()
    add_ref(branch_name, get_commit_by_branch('HEAD'))

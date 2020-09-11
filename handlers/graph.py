import re
from pathlib import Path

from graphviz import Digraph

from consts import IMAGES_FOLDER
from helpers import get_commit_by_branch, get_wit_repo_path, get_all_branches
from wit_errors import WitCommitNotFound


def graph(all_flag):
    repository_path = get_wit_repo_path()
    curent_commit = get_commit_by_branch('HEAD')

    g = Digraph('G', filename=str(
        Path(repository_path, 'wit_graph')), format='png')

    for branch in list(get_all_branches()):
        g.attr('node', shape='box', size='6,6')
        g.node(branch)

        g.attr('node', color='lightblue2', style='filled', shape='circle')
        g.edge(branch, break_line(get_commit_by_branch(branch)))

    if all_flag:
        draw_all_nodes(g, repository_path).view()
    else:
        draw_current_branch(g, repository_path, curent_commit).view()


def draw_all_nodes(g, repository_path):
    for item in Path(repository_path, IMAGES_FOLDER).iterdir():
        if item.is_file():
            if item.suffix == '.txt':
                curent_commit = item.stem
                parent_commit = read_parent(item)
                if parent_commit != 'None':
                    g.edge(break_line(parent_commit),
                           break_line(curent_commit))
    return g


def draw_current_branch(g, repository_path, curent_commit):
    prev_commit = curent_commit
    curent_commit = get_parent_commit(repository_path, curent_commit)
    while curent_commit != 'None':
        g.edge(break_line(curent_commit), break_line(prev_commit))
        prev_commit = curent_commit
        curent_commit = get_parent_commit(repository_path, curent_commit)
    return g


def get_parent_commit(repository_path, commit_id):
    info_file = Path(repository_path, IMAGES_FOLDER,
                     commit_id).with_suffix('.txt')
    if not info_file.exists():
        raise WitCommitNotFound()
    return read_parent(info_file)


def read_parent(file):
    info = file.open().read().split()
    return list(filter(lambda row: "parent" in row, info))[0].split("=")[1]


# some string braker code for lazy people
# https://stackoverflow.com/questions/23439082/insert-into-every-4th-character


def break_line(s):
    return re.sub(r'((?:(?=(10|.))\2){10})(?!$)', r'\1\n', s)

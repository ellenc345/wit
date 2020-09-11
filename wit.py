import sys

from consts import COMMANDS

from handlers.add import add
from handlers.branch import branch
from handlers.checkout import checkout
from handlers.commit import commit
from handlers.graph import graph
from handlers.init import init
from handlers.merge import merge
from handlers.status import status

from logger import define_logging

from wit_errors import WitError


if __name__ == '__main__':
    try:
        if not len(sys.argv):
            raise ValueError('No params was provided')
        command = sys.argv[1]
        if command not in COMMANDS:
            raise ValueError(f'Usage: python <witpath> <commnd: {COMMANDS}>')
        if command == 'init':
            init()
        if command == 'add':
            add(sys.argv[2])
        if command == 'commit':
            commit(sys.argv[2])
        if command == 'status':
            status()
        if command == 'checkout':
            checkout(sys.argv[2])
        if command == 'graph':
            is_all = False
            if len(sys.argv) == 3:
                is_all = sys.argv[2] == '--all'
            graph(is_all)
        if command == 'branch':
            branch(sys.argv[2])
        if command == 'merge':
            merge(sys.argv[2])
    except (ValueError, WitError) as err:
        logger = define_logging(__name__)
        logger.error(f'{err}\nAborted')

# Use Exsample:
# cd C:\Users\ellen\OneDrive\Documents\py-course\week1
# python "C:\Users\ellen\OneDrive\Documents\py-course\week10\Upload_175\wit.py" init
# python "C:\Users\ellen\OneDrive\Documents\py-course\week10\Upload_175\wit.py" add "images\logo.jpg"
# python "C:\Users\ellen\OneDrive\Documents\py-course\week10\Upload_175\wit.py" status
# python "C:\Users\ellen\OneDrive\Documents\py-course\week10\Upload_175\wit.py" checkout ffe43abb5bb4b4f7b7ab4434c37c883470aeee27
# python "C:\Users\ellen\OneDrive\Documents\py-course\week10\Upload_175\wit.py" graph
# python "C:\Users\ellen\OneDrive\Documents\py-course\week10\Upload_175\wit.py" branch "branch-name"
# python "C:\Users\ellen\OneDrive\Documents\py-course\week10\Upload_175\wit.py" merge "branch-name"
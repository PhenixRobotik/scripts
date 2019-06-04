#!/bin/env python3

from clone_or_pull_all import *

tag_name = 'cdr2019'
tag_message = 'La Coupe est passée, time to tag.'

def tag_repo(repo):
    dir = clone_dir + '/' + repo['name']

    print(dir)
    if os.path.exists(dir):
        cmd = [ 'git', '-C', dir, 'tag', '-a', tag_name, '-m', tag_message ]

    proc = subprocess.Popen(cmd,
        stderr = subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    return proc.returncode, stderr.decode('utf-8')


def push_repo(repo):
    dir = clone_dir + '/' + repo['name']

    print(dir)
    if os.path.exists(dir):
        cmd = [ 'git', '-C', dir, 'push', '--tags' ]

    proc = subprocess.Popen(cmd,
        stderr = subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    return proc.returncode, stderr.decode('utf-8')


if __name__ == '__main__':
    process_repositories('tag', tag_repo)
    process_repositories('tag', push_repo)

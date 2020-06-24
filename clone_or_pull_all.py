#!/usr/bin/env python3

import requests
import json
import os
import sys
import subprocess

import multiprocessing

# user_path='users/salamandar'
user_path = 'orgs/phenixrobotik'
script_dir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()
clone_dir = current_dir
use_ssh = True


def fetch_repos_list(user):
    def page_url(user, page, count):
        return ('https://api.github.com/' + user + '/repos'
                + '?page=' + str(page)
                + '&per_page=' + str(count))

    page = 1
    repos = []
    while True:
        count = 1000
        data = requests.get(page_url(user_path, page, count))
        list = json.loads(data.text)

        repos += list

        if len(list) < count:
            break
        else:
            page += 1
    return repos


def clone_or_pull(repo):
    dir = clone_dir + '/' + repo['name']

    print(dir)
    if os.path.exists(dir):
        cmd = [ 'git', '-C', dir, 'pull', '--recurse-submodules' ]
    else:
        url = repo['ssh_url'] if use_ssh else repo['html_url']
        cmd = [ 'git', 'clone', '--recursive', url, dir ]

    proc = subprocess.Popen(cmd,
        stderr = subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    return proc.returncode, stderr.decode('utf-8')


def process_repositories(process_name, function):
    repos_list = fetch_repos_list(user_path)
    # for repo in repos_list:
    #     clone_or_pull(repo)

    pool = multiprocessing.Pool()
    results = pool.map(function, repos_list)
    results_zipped = tuple(zip(repos_list, results))

    for i in results_zipped:
        if i[1][0] != 0:
            print('Could not', process_name, 'repo', i[0]['name'])
            print(i[1][1])


if __name__ == '__main__':
    # Update script then call self
    if len(sys.argv) > 1 and sys.argv[1] == 'no-recall':
        pass
    else:
        clone_or_pull({'name': 'scripts'})
        os.execv(sys.executable, ['python'] + sys.argv + ['no-recall'])

    process_repositories('update', clone_or_pull)

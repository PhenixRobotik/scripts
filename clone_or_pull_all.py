#!/bin/env python3

import requests
import json
import os

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
    if use_ssh:
        url = repo['ssh_url']
    else:
        url = repo['html_url']

    print(dir)
    if os.path.exists(dir):
        return os.system('git -C ' + dir + ' pull --recurse-submodules')
    else:
        return os.system('git clone --recursive ' + url + ' ' + dir)


if __name__ == '__main__':
    repos_list = fetch_repos_list(user_path)
    # for repo in repos_list:
    #     clone_or_pull(repo)

    pool = multiprocessing.Pool()
    results = pool.map(clone_or_pull, repos_list)
    results_zipped = tuple(zip(repos_list, results))

    for i in results_zipped:
        if i[1] != 0:
            print('Could not update repo', i[0]['name'])

#!/bin/env python3

import requests
import json
import os

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
    repos= []
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
        os.system('git -C ' + dir + ' pull')
    else:
        os.system('git clone --recursive ' + url + ' ' + dir)



for repo in fetch_repos_list(user_path):
    clone_or_pull(repo)

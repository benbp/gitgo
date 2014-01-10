#!/usr/bin/python

import subprocess as sproc
import os
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('top_dir', nargs='?', default=os.getcwd())
    return parser.parse_args()


def find_git_repos(dir):
    git_repos = []
    if not os.path.isdir(dir):
        return False
    os.chdir(dir)
    try:
        sproc.check_output(["git rev-parse"], shell=True, stderr=sproc.PIPE)
        return [dir]
    except sproc.CalledProcessError:
        pass
    for d in os.listdir(dir):
        d = os.path.join(dir, d)
        repos = find_git_repos(d)
        if repos:
            git_repos = git_repos + repos
    return git_repos


def main():
    args = parse_args()
    print find_git_repos(args.top_dir)


if __name__ == '__main__':
    main()

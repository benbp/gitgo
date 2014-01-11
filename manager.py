#!/usr/bin/python

import subprocess
import os
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('args', nargs='+',
                       help='Enter any number of git commands and directories')
    args = parser.parse_args()
    paths, commands = [], []
    for a in args.args:
        if os.path.isdir(a):
            paths.append(a)
        else:
            commands.append(a.split(' '))
    if not paths:
        paths.append(os.getcwd())
    return (commands, paths)



def find_git_repos(path):
    git_repos = []
    if not os.path.isdir(path):
        return False
    os.chdir(path)
    try:
        subprocess.check_output(["git rev-parse"], shell=True, stderr=subprocess.PIPE)
        return [path]
    except subprocess.CalledProcessError:
        pass
    for d in os.listdir(path):
        d = os.path.join(path, d)
        repos = find_git_repos(d)
        if repos:
            git_repos = git_repos + repos
    return git_repos


def exec_git_command(path, cmd):
    path = os.path.abspath(path)
    git_repos = find_git_repos(path)
    for repo in git_repos:
        os.chdir(repo)
        print "..." + repo.replace(path, '')
        try:
            print subprocess.check_output(["git"] + cmd)
        except:
            print 'FAILURE'
            pass


def main():
    (commands, paths) = parse_args()
    #find_git_repos(args.top_dir)
    print commands, paths
    for cmd in commands:
        print "*"*80
        print "Running 'git " + ' '.join(cmd) + "' in:"
        print "*"*80
        for path in paths:
            exec_git_command(path, cmd)


if __name__ == '__main__':
    main()

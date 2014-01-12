#!/usr/bin/python

import subprocess
import os
from argparse import ArgumentParser, RawTextHelpFormatter


def parse_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
        description="Tool for managing git repositories "\
        "within a golang workspace. Run git commands across directories, e.g. "\
        "switch multiple branches before a build.\n\n"\
        "Examples:\n"\
        "# Show branches and remotes of selected repositories\n"\
        "gitgo 'branch -a' 'remote show' -r packer gophercloud perigee\n"\
        "# git pull and checkout new branch on all subdirectories of repo1 "\
        "and repo2\n"\
        "gitgo ~/repo1 ~/repo2 pull 'checkout -b new_branch'\n"\
        "# get status of all repositories owned by benbp\n"\
        "gitgo status -o benbp\n"\
        )
    parser.add_argument('args', nargs='+',
                       help="Enter any number of git commands and directories.")
    parser.add_argument('-r', '--directories', dest='repos', nargs='+',
                       help="Specify repository name. Will run commands on "\
                                "repositories within the search path.")
    parser.add_argument('-o', '--owner', dest='owners', nargs='+', default=[],
                       help="Specify repository owner. Will run commands on "\
                               "repositories within the folder of <owner>.")
    parser.add_argument('-c', '--use-cwd', dest='use_cwd', action='store_true',
                        default=[],
                       help="Search/run within current directory instead of "\
                               "within the $GOPATH")
    args = parser.parse_args()
    paths, commands = [], []
    for a in args.args:
        if os.path.isdir(a):
            paths.append(a)
        else:
            commands.append(a.split(' '))
    if args.use_cwd:
        paths.append(os.getcwd())
    elif not paths:
        go_src_path = os.path.join(os.environ['GOPATH'], 'src')
        paths.append(go_src_path)
    options = {'owners': args.owners, 'repos': args.repos}
    return (commands, paths, options)


def find_git_repos(path, matches=[]):
    git_repos = []
    if not os.path.isdir(path):
        return []
    os.chdir(path)
    relevant_path = path.replace(os.environ['GOPATH'], '')
    if not matches or [m for m in matches if m in relevant_path]:
        try:
            r = subprocess.check_output(["git rev-parse --is-inside-work-tree"],
                                            shell=True, stderr=subprocess.PIPE)
            if r == 'true\n':
                return [path]
        except subprocess.CalledProcessError:
            pass
    for d in os.listdir(path):
        d = os.path.join(path, d)
        repos = find_git_repos(d, matches)
        if repos:
            git_repos = git_repos + repos
    return git_repos


def run_all(commands, paths, matches=[]):
    for cmd in commands:
        print "*"*80
        print "Running 'git " + ' '.join(cmd) + "' in:"
        print "*"*80
        for path in paths:
            abspath = os.path.abspath(path)
            git_repos = find_git_repos(abspath, matches)
            for repo in git_repos:
                os.chdir(repo)
                print "..." + repo.replace(path, '')
                try:
                    print subprocess.check_output(["git"] + cmd)
                except:
                    print "FAILURE\n"


def main():
    (commands, paths, options) = parse_args()
    if options['repos']:
        run_all(commands, paths, options['repos'])
    if options['owners']:
        run_all(commands, paths, options['owners'])
    if not options['repos'] and not options['owners']:
        run_all(commands, paths)


if __name__ == '__main__':
    main()

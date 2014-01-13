#!/usr/bin/python

#TODO: add a flag for different commands per repo, e.g.
#           -x 'checkout master' repo1 repo2 -x 'checkout testing' repo3
#TODO: switch to argparse subcommands so that -p flag cannot be used with
# anything else

import subprocess
import os
import yaml
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

YAML_TEMPLATE = os.path.join(os.environ['HOME'], ".gitgo.yaml")

def parse_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
        description="Tool for managing git repositories "\
        "within a golang workspace. Run git commands across directories, e.g. "\
        "switch multiple branches before a build.\n\n"\
        "Examples:\n"\
        "# Show branches and remotes of selected repositories\n"\
        "   gitgo 'branch -a' 'remote show' -r packer gophercloud perigee\n"\
        "# git pull and checkout new branch on all subdirectories of repo1 "\
        "and repo2\n"\
        "   gitgo pull 'checkout -b new_branch' -r repo1 repo2\n"\
        "# get status of all repositories owned by benbp\n"\
        "   gitgo status -o benbp\n"\
        "# Use a pre-defined project defined in ~/.gitgo.yaml.\n"\
        "   gitgo -p <project_name>\n"
        )
    parser.add_argument('args', nargs='*',
                        help="Enter any number of git commands and directories.")
    parser.add_argument('-r', '--repos', dest='repos', nargs='+',
                        help="Specify repository names. Will run commands on "\
                                "repositories within the search path.")
    parser.add_argument('-o', '--owners', dest='owners', nargs='+',
                        help="Specify repository owners. Will run commands on "\
                                "repositories within the folder of <owner>.")
    parser.add_argument('-c', '--use-cwd', dest='use_cwd', action='store_true',
                        default=False,
                        help="Search/run within current directory instead of "\
                                "within the $GOPATH")
    parser.add_argument('-p', '--use-project', dest='project', nargs=1,
                        help="Use project pre-defined in the template file "\
                                "(~/.gitgo.yaml).")
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
    if (args.owners or args.repos) and not args.args:
        print "Error: no git commands entered."
        sys.exit()
    if args.project:
        project = args.project[0]
    else:
        project = None
    return (commands, paths, options, project)


def template_reader():
    stream = open(YAML_TEMPLATE, 'r')
    try:
        template = yaml.load(stream)
    finally:
        stream.close()
    return template


def template_writer(template_dump):
    stream = open(YAML_TEMPLATE, 'w')
    try:
        yaml.dump(template_dump, default_flow_style=False)
    finally:
        stream.close()


def exec_template(project):
    template = template_reader()
    if project not in template:
        return None
    block = template[project]
    for rule in block:
        site = rule['site']
        owner = rule['owner']
        repo = rule['repo']
        branch = rule['branch']
        path = os.path.join(os.environ['GOPATH'], 'src', site, owner, repo)
        cmd = ['checkout', branch]
        run_all([cmd], [path])


def find_git_repos(path, matches):
    git_repos = []
    if not os.path.isdir(path):
        return None
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


def run_all(commands, paths, matches=None):
    for cmd in commands:
        print "*"*80
        print "Running 'git " + ' '.join(cmd) + "' in:"
        print "*"*80
        for path in paths:
            abspath = os.path.abspath(path)
            git_repos = find_git_repos(abspath, matches)
            if not git_repos:
                return
            for repo in git_repos:
                os.chdir(repo)
                print "..." + repo.replace(path, '')
                try:
                    print subprocess.check_output(["git"] + cmd)
                except subprocess.CalledProcessError:
                    print "FAILURE\n"


def main():
    (commands, paths, options, project) = parse_args()
    if options['repos']:
        run_all(commands, paths, options['repos'])
    if options['owners']:
        run_all(commands, paths, options['owners'])
    if project:
        exec_template(project)
    if not options['repos'] and not options['owners'] and not project:
        run_all(commands, paths)


if __name__ == '__main__':
    main()
